# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import enum
import re
import sys
import typing as t
from abc import abstractmethod, ABCMeta
from collections.abc import Iterable
from time import sleep

import bs4
from bs4 import BeautifulSoup as Soup, Tag
from es7s_commons import columns, to_subscript, to_superscript
from requests import Response

from es7s.shared import requester, get_stdout, get_logger, Styles as BaseStyles
from ._base import _BaseAction

import pytermor as pt

from ..shared.enum import WordType


class SemAction(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        self._requester = requester.Requester()
        self._last_response: Response | None = None
        self._last_soup: Soup | None = None
        self._run(**kwargs)

    def _run(self, **kwargs):
        self._run_once(**kwargs)

    def _run_once(self, word: str | t.Iterable[str], raw: bool):
        stdout = get_stdout()
        text = None

        self._last_response = self._make_request(word)
        try:
            text = self._last_response.text
            if "<html" not in text.lower():
                text = f"<html>{self._last_response.text}</html>"

            self._last_soup = bs4.BeautifulSoup(text, features="lxml")

            if answer := self._find_results(self._last_soup):
                parsed_results = [*self._parse_results(answer)]
                if sys.stdout.isatty():
                    c, ts = columns(parsed_results)
                    get_stdout().echoi_rendered(c)
                    get_logger().debug(ts)
                else:
                    for pres in parsed_results:
                        get_stdout().echo_rendered(pres)
            else:
                get_logger().warning("No results")

        except Exception as e:
            get_logger().exception(e)
            self._last_soup = None

        if raw:
            if self._last_soup:
                stdout.echo(self._last_soup.prettify())
            else:
                stdout.echo(text)

    def _get_request_headers(self) -> dict:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }

    @abstractmethod
    def _make_request(self, word: str | t.Iterable[str]) -> Response:
        ...

    @abstractmethod
    def _find_results(self, html: Soup) -> Soup:
        ...

    @abstractmethod
    def _parse_results(self, results: Soup) -> Iterable[pt.RT]:
        ...


class action_complement(SemAction, _BaseAction):
    URL_TEMPLATE = f"https://sinonim.org/kb/%s"

    def _make_request(self, word: t.Iterable[str]) -> Response:
        return self._requester.make_request(
            self.URL_TEMPLATE % " ".join(word),
            headers=self._get_request_headers(),
        )

    def _find_results(self, html: Soup) -> Soup:
        return html.find(id="assocPodryad")

    def _parse_results(self, answer: Soup) -> Iterable[str]:
        for result in answer.find_all(class_="riLi"):
            yield result.text


class action_rhymes(SemAction, _BaseAction):
    URL_TEMPLATE = "https://rifmovka.ru/rifma/{}"
    URL_NEXT_TEMPLATE = "https://rifmovka.ru/rhyme/more?hash={hash}&last={end}"

    class XEnd(int, pt.ExtendedEnum):
        X_END_INITIAL = -1
        X_END_PROCEED = 0
        X_END_EOF = 1

    class Styles(BaseStyles):
        def __init__(self):
            self.ACCENT_LETTER = pt.FrozenStyle(fg=pt.cv.GRAY_100, bold=True)
            self.WORD_CLASSES = {
                WordType.NOUN: pt.cv.GREEN,
                WordType.ADJ: pt.cv.YELLOW,
                WordType.VERB: pt.cv.BLUE,
                WordType.DPART: pt.cv.CYAN,
                WordType.OTHER: pt.cv.GRAY_50,
            }

    def __init__(
        self, word: str, no_input: bool, same_size: bool, size: int, _type: WordType, **kwargs
    ):
        self._paginate_args = {
            "hash": None,
            "end": self.XEnd.X_END_INITIAL,
        }
        self._is_first_request = True
        self._interactive = not no_input and sys.stdin.isatty()
        # INTERACTIVE MODE | stdin=tty | stdin!=tty |
        # -----------------|-----------|------------|
        # no_input=True    |    OFF    |     OFF    |
        # no_input=False   |    ON     |     OFF    |
        get_logger().debug(f"Interactive mode is " + ("OFF", "ON")[self._interactive])

        self._filter_size = size
        self._filter_type = _type
        if same_size:
            self._filter_size = self._count_syllables(word)

        self._styles = self.Styles()
        super().__init__(word=word, **kwargs)

    def _run(self, **kwargs):
        self._run_loop(**kwargs)

    def _run_loop(self, **kwargs):
        while True:
            self._run_once(**kwargs)

            try:
                self._extract_next_query_params()
                if self._paginate_args["end"] == self.XEnd.X_END_EOF:
                    break
                if not self._confirm_next_page():
                    break
            except Exception as e:
                get_logger().error(e)
                return

    def _extract_next_query_params(self):
        if self._is_first_request:
            if not self._last_soup:
                raise ValueError("No previous HTML page available")

            hash_raw = self._last_soup.find("body")["data-hash"]
            hash, _ = hash_raw.split(";")  # "<similar>;<interesting>"
            self._paginate_args.update({"hash": hash})
            self._is_first_request = False
            return

        if not self._last_response:
            raise ValueError("No previous HTTP response available")

        headers = self._last_response.headers
        self._paginate_args.update(
            {
                "hash": headers.get("X-Hash"),
                "end": self.XEnd.resolve_by_value(int(headers.get("X-End"))),
            }
        )

    def _confirm_next_page(self) -> bool:
        if self._interactive:
            print("Continue? [Y/n]: ", file=sys.stderr)
            return input().strip().lower() != "n"
        sleep(0.1)
        return True

    def _make_request(self, word: str) -> Response:
        url = self.URL_TEMPLATE.format(word)
        if not self._is_first_request:
            url = self.URL_NEXT_TEMPLATE.format(**self._paginate_args)

        return self._requester.make_request(url, headers=self._get_request_headers())

    def _find_results(self, html: Soup) -> Soup:
        if self._is_first_request:
            return html.find(itemprop="acceptedAnswer")
        return html

    def _parse_results(self, answer: Soup) -> Iterable[pt.RT]:
        accent_st = self._styles.ACCENT_LETTER
        for result in answer.find_all(name="li"):
            syllables = self._count_syllables(str(result))
            if self._filter_size and self._filter_size != syllables:
                continue

            word_classes = [*self._extract_word_classes(result)]
            if self._filter_type and self._filter_type not in word_classes:
                continue

            frags = (str(result),)
            if result.has_attr("data-masked"):
                result_str = result["data-masked"]
                if m := re.search(";(.);", result_str):
                    frags = (result_str[: m.start()], m.group(1), accent_st, result_str[m.end() :])
                    syllables = self._count_syllables(result_str)

            elif len(result.contents) > 0:
                frags = []
                for cpart in result.contents:
                    frags.append(cpart.text)
                    if isinstance(cpart, Tag):
                        frags.append(accent_st)
                syllables = self._count_syllables(result.text)

            frags = [
                *self._format_type(result, syllables),
                " ",
                *frags,
                " ",
            ]
            yield pt.Text(*frags)

    def _extract_word_classes(self, result: Soup) -> list[str]:
        for wc in result["class"]:
            if wc in ["vis", "off", "rare"]:
                continue
            if wc not in self._styles.WORD_CLASSES.keys():
                get_logger().warning(f"Unknown word class: {wc}")
                break
            yield wc

    def _format_type(self, result: Soup, syllables: int) -> list[pt.RT | tuple[pt.RT, pt.FT]]:
        frags: list[pt.RT | tuple[pt.RT, pt.FT]] = [to_superscript(str(syllables))]

        word_class = [wc for wc in result["class"] if wc not in ["vis", "off", "rare"]]
        for wc in word_class:
            if wc not in self._styles.WORD_CLASSES.keys():
                get_logger().warning(f"Unknown word class: {wc}")
                break
            frags.append((wc.lower()[0], self._styles.WORD_CLASSES.get(wc)))

        if "off" in result["class"]:
            frags.append(("!", pt.Styles.ERROR_LABEL))
        elif "rare" in result["class"]:
            frags.append(("-", pt.cv.MAGENTA))

        while len(frags) < 3:
            frags.append(" ")
        return frags

    def _count_syllables(self, word: str) -> int:
        return len(re.findall(r"[уеёыаоэяию]", word))
