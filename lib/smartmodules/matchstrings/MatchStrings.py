from __future__ import annotations
import importlib, pkgutil
from typing import Dict, List

# Global registries (service -> bucket -> [regex patterns])
products_match: Dict[str, Dict[str, List[str]]] = {}
options_match:  Dict[str, Dict[str, List[str]]] = {}
vulns_match:    Dict[str, Dict[str, List[str]]] = {}
os_match:       Dict[str, Dict[str, List[str]]] = {}
creds_match:    Dict = {}

__all__ = [
    "products_match","options_match","vulns_match","os_match","creds_match",
    "get_products_match","get_options_match","get_vulns_match","get_os_match","get_creds_match",
]

_LOADED = False

def _load_pkg(modname: str) -> None:
    try:
        pkg = importlib.import_module(modname)
    except Exception:
        return
    prefix = pkg.__name__ + "."
    for _, name, _ in pkgutil.iter_modules(pkg.__path__, prefix):
        importlib.import_module(name)

def _ensure_loaded() -> None:
    global _LOADED, creds_match
    if _LOADED:
        return
    _load_pkg("lib.smartmodules.matchstrings.products")
    _load_pkg("lib.smartmodules.matchstrings.options")
    _load_pkg("lib.smartmodules.matchstrings.vulns")
    _load_pkg("lib.smartmodules.matchstrings.os")
    _load_pkg("lib.smartmodules.matchstrings.creds")
    # Import creds_match from registry after loading
    from lib.smartmodules.matchstrings.registry import creds_match as reg_creds
    creds_match.update(reg_creds)
    _LOADED = True

def get_products_match(): _ensure_loaded(); return products_match
def get_options_match():  _ensure_loaded(); return options_match
def get_vulns_match():    _ensure_loaded(); return vulns_match
def get_os_match():       _ensure_loaded(); return os_match
def get_creds_match():    _ensure_loaded(); return creds_match
