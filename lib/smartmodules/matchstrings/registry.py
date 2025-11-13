"""Shared registries for SmartModule matchstrings.

This module isolates the global dictionaries that SmartModules populate so
that individual per-service modules can import them without creating circular
imports with :mod:`lib.smartmodules.matchstrings.MatchStrings`.
"""
from collections import defaultdict

# ------------------------------------------------------------------------------------
# Credentials matchers, indexed by service and tool.
creds_match = {}

# ------------------------------------------------------------------------------------
# Specific options for contextual information enrichment.
options_match = {}

# ------------------------------------------------------------------------------------
# Products registry, grouped by service and product type.
products_match = defaultdict(dict)

# ------------------------------------------------------------------------------------
# Vulnerability strings harvested from tool outputs.
vulns_match = {}

# ------------------------------------------------------------------------------------
# Operating system fingerprints.
os_match = {}

# ------------------------------------------------------------------------------------
# Shared regexp placeholder used by multiple product matchstrings.
VERSION_REGEXP = '(?P<version>[0-9.]*[0-9])?'

__all__ = [
    'creds_match',
    'options_match',
    'products_match',
    'vulns_match',
    'os_match',
    'VERSION_REGEXP',
]
