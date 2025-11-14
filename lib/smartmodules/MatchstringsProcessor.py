from __future__ import annotations
import re
from typing import Any, Dict, Iterable, List, Mapping, Optional

# Lazy registries
from lib.smartmodules.matchstrings.MatchStrings import (
    get_products_match, get_options_match, get_vulns_match, get_os_match, get_creds_match
)

def _concat_outputs(outputs: Iterable[Any]) -> str:
    parts: List[str] = []
    for o in outputs or []:
        # tolerate both objects with .output/.stdout and raw strings
        for attr in ("output", "stdout", "stderr"):
            v = getattr(o, attr, None)
            if isinstance(v, str) and v:
                parts.append(v)
        if isinstance(o, str):
            parts.append(o)
    return "\n".join(parts)

def _ensure_regexes(patterns: Iterable[str]) -> List[re.Pattern]:
    rx: List[re.Pattern] = []
    for p in patterns:
        try:
            rx.append(re.compile(p, re.I))
        except re.error:
            rx.append(re.compile(rf"^{re.escape(p)}$", re.I))
    return rx

class MatchstringsProcessor:
    """
    Minimal, side-effect-free processor used by SmartStart.
    It scans command outputs against matchstring registries and records findings.
    """

    def __init__(self, service: Any, outputs: Iterable[Any], settings: Optional[Mapping[str, Any]] = None) -> None:
        self.service_name = getattr(service, "name", str(service)).lower()
        self.outputs = list(outputs or [])
        self.settings = dict(settings or {})
        self.text = _concat_outputs(self.outputs)

        # snapshots of registries at init time
        self.products_match = get_products_match()
        self.options_match  = get_options_match()
        self.vulns_match    = get_vulns_match()
        self.os_match       = get_os_match()
        self.creds_match    = get_creds_match()

        # results
        self.found_products: Dict[str, List[str]] = {}
        self.found_options:  Dict[str, List[str]] = {}
        self.found_vulns:    Dict[str, List[str]] = {}
        self.found_os:       Dict[str, List[str]] = {}
        self.found_creds:    List[Dict[str, str]] = []

    # ---- detectors ----

    def detect_specific_options(self) -> Dict[str, List[str]]:
        buckets = self.options_match.get(self.service_name, {})
        out: Dict[str, List[str]] = {}
        for bucket, pats in buckets.items():
            rx = _ensure_regexes(pats)
            hits = sorted({p.pattern for p in rx if p.search(self.text)})
            if hits:
                out[bucket] = hits
        self.found_options = out
        return out

    def detect_products(self) -> Dict[str, List[str]]:
        buckets = self.products_match.get(self.service_name, {})
        out: Dict[str, List[str]] = {}
        for bucket, pats in buckets.items():
            rx = _ensure_regexes(pats)
            hits = sorted({p.pattern for p in rx if p.search(self.text)})
            if hits:
                out[bucket] = hits
        self.found_products = out
        return out

    def detect_vulns(self) -> Dict[str, List[str]]:
        buckets = self.vulns_match.get(self.service_name, {})
        out: Dict[str, List[str]] = {}
        for bucket, pats in buckets.items():
            rx = _ensure_regexes(pats)
            hits = sorted({p.pattern for p in rx if p.search(self.text)})
            if hits:
                out[bucket] = hits
        self.found_vulns = out
        return out

    def detect_os(self) -> Dict[str, List[str]]:
        buckets = self.os_match.get("generic", {})
        out: Dict[str, List[str]] = {}
        for bucket, pats in buckets.items():
            rx = _ensure_regexes(pats)
            hits = sorted({p.pattern for p in rx if p.search(self.text)})
            if hits:
                out[bucket] = hits
        self.found_os = out
        return out

    def detect_credentials(self) -> List[Dict[str, str]]:
        """Detect credentials from command output."""
        creds = []
        service_creds = self.creds_match.get(self.service_name, {})
        
        for tool_name, patterns_dict in service_creds.items():
            for pattern, cred_info in patterns_dict.items():
                try:
                    regex = re.compile(pattern, re.IGNORECASE | re.DOTALL)
                    for match in regex.finditer(self.text):
                        cred_dict = {
                            'type': cred_info.get('type', 'credentials'),
                        }
                        # Extract username/password from named groups
                        if 'm1' in match.groupdict():
                            cred_dict['username'] = match.group('m1')
                        if 'm2' in match.groupdict():
                            cred_dict['password'] = match.group('m2')
                        if cred_dict.get('username') or cred_dict.get('password'):
                            creds.append(cred_dict)
                except re.error:
                    pass
        
        self.found_creds = creds
        return creds
