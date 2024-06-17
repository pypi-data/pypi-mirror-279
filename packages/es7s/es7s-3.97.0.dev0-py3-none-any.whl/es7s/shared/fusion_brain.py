# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import json
from functools import cached_property
from logging import getLogger
from uuid import UUID

import requests
from es7s_commons import format_attrs
from requests import Response


class FusionBrainAPI:
    HOST = "https://api-key.fusionbrain.ai/"

    def __init__(self, api_key: str, secret_key: str):
        self._api_key = api_key
        self._secret_key = secret_key
        self._model_id: int | None = None
        self._style_names: list[str] = []

    @cached_property
    def _headers(self) -> dict:
        return {
            "X-Key": f"Key {self._api_key}",
            "X-Secret": f"Secret {self._secret_key}",
        }

    def copy(self) -> "FusionBrainAPI":
        c = FusionBrainAPI(self._api_key, self._secret_key)
        c._model_id = self._model_id
        c._style_names = c._style_names.copy()
        return c

    def fetch_model(self) -> int:
        try:
            response = requests.get(self.HOST + "key/api/v1/models", headers=self._headers)
            if not response.ok:
                raise RuntimeError(
                    f"Failed to fetch model ID (HTTP {response.status_code}: {response!r}"
                )
            data = response.json()
            _get_logger().debug("< " + format_attrs(data))
            self._model_id = int(data[0]["id"])
            return self._model_id
        except (TypeError, ValueError, requests.RequestException) as e:
            raise RuntimeError(f"Failed to get model ID: {e}")

    def fetch_styles(self) -> list[str]:
        response = requests.get("https://cdn.fusionbrain.ai/static/styles/api")
        if not response.ok:
            getLogger().warning(f"Fetched to fetch styles: {response!r}")
            return []

        data = response.json()
        _get_logger().debug("< " + format_attrs(data))

        self._style_names.clear()
        if not data:
            getLogger().warning("Fetched empty style list")
        for style in data:
            self._style_names.append(style.get("name"))
        return self._style_names

    def generate(
        self,
        prompt: str,
        negprompt: list[str] = None,
        style: str = None,
        size=(1024, 1024),
        images=1,
    ) -> UUID:
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": size[0],
            "height": size[1],
            "generateParams": {"query": f"{prompt}"},
        }
        if negprompt:
            params.update({"negativePromptUnclip": ",".join(negprompt)})
        if style:
            params.update({"style": style})

        data = {
            "model_id": (None, self._model_id),
            "params": (None, json.dumps(params), "application/json"),
        }
        _get_logger().debug("> " + format_attrs(data))
        response = requests.post(
            self.HOST + "key/api/v1/text2image/run",
            headers=self._headers,
            files=data,
            timeout=30,
        )
        data = response.json()
        _get_logger().debug("< " + format_attrs(data))

        return UUID(data["uuid"])

    def check_generation(self, request_id: UUID) -> tuple[list[str], bool | None, Response]:
        response = requests.get(
            self.HOST + "key/api/v1/text2image/status/" + str(request_id),
            headers=self._headers,
            timeout=30,
        )
        try:
            data = response.json()
        except ValueError:
            return [], None, response
        _get_logger().debug("< " + format_attrs(data, truncate=4096))

        if data["status"] == "DONE":
            return data.get("images", []), data.get("censored"), response
        return [], None, response


def _get_logger():
    return getLogger(__package__)
