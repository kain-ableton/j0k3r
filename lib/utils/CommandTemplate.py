#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helper utilities to expand Jok3r command templates."""

from urllib.parse import urlparse

from tld import get_tld

try:
    # ``TldDomainNotFound`` lived in ``tld`` until 0.13, newer releases expose
    # it from ``tld.exceptions`` only. Attempt the legacy import first so both
    # series keep working without forcing a specific dependency pin.
    from tld import TldDomainNotFound  # type: ignore
except ImportError:  # pragma: no cover - depends on installed ``tld`` version
    from tld.exceptions import TldDomainNotFound

from lib.core.Config import TOOLBOX_DIR, WEBSHELLS_DIR, WORDLISTS_DIR
from lib.utils.NetUtils import NetUtils


def _safe(value):
    """Return a safe string representation for replacement tokens."""
    return value or ''


def _extract_domain(url):
    if not url:
        return ''

    try:
        return get_tld(url, as_object=True, fail_silently=True).fld
    except (TldDomainNotFound, AttributeError, ValueError):
        parsed = urlparse(url)
        return parsed.hostname or ''


def _extract_path(url):
    if not url:
        return ''

    return urlparse(url).path or '/'


def expand_custom_command(template, target):
    """Expand the supported tokens inside a custom command template."""
    if not template:
        return ''

    mapping = {
        '[IP]': _safe(target.get_ip()),
        '[URL]': _safe(target.get_url()),
        '[HOST]': _safe(target.get_host()),
        '[PORT]': str(target.get_port()),
        '[URIPATH]': _safe(_extract_path(target.get_url())),
        '[PROTOCOL]': _safe(target.get_protocol()),
        '[SERVICE]': _safe(target.get_service_name()),
        '[TOOLBOXDIR]': TOOLBOX_DIR,
        '[WEBSHELLSDIR]': WEBSHELLS_DIR,
        '[WORDLISTSDIR]': WORDLISTS_DIR,
        '[LOCALIP]': NetUtils.get_local_ip_address(),
        '[DOMAIN]': _safe(_extract_domain(target.get_url())),
    }

    expanded = template
    for token, value in mapping.items():
        expanded = expanded.replace(token, value)

    return expanded
