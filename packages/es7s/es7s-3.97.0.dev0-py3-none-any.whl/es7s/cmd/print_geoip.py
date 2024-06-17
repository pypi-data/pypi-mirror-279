# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from dataclasses import asdict
from ipaddress import IPv4Address, IPv6Address

import pytermor as pt

from es7s.shared import GeoIpResolver, VarTableStyles, get_stdout, format_variable
from ._base import _BaseAction


class action(_BaseAction):
    def __init__(self, **kwargs):
        self._geo_ip_resolver = GeoIpResolver()
        self._vts = VarTableStyles()
        self._run(**kwargs)

    def _run(self, address: IPv4Address | IPv6Address = None):
        kv = asdict(self._geo_ip_resolver.make_request(address))
        longest_key = max(len(k) for k in kv.keys())
        for k, v in kv.items():
            get_stdout().echo_rendered(
                pt.Fragment(k.rjust(longest_key), self._vts.VARIABLE_KEY_FMT)
                + pt.Fragment(": ", self._vts.VARIABLE_PUNCT_FMT)
                + format_variable(v)
            )
