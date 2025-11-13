#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###
# SmartModules > Matchstrings Processor (refactor)
###
import re
import regex
from typing import Any, Dict, Iterable, Optional, Tuple

from lib.output.Logger import logger
from lib.utils.StringUtils import StringUtils
from lib.smartmodules.matchstrings.registry import (
    creds_match,
    options_match,
    products_match,
    vulns_match,
    os_match,
    VERSION_REGEXP,
)


class MatchstringsProcessor:
    """Processes matchstrings to detect credentials, options, products, vulns and OS.
    """

    def __init__(
        self,
        service,
        tool_name: str,
        cmd_output: Optional[str],
        context_updater,
    ):
        self.service = service
        self.tool_name = tool_name
        self.cmd_output = cmd_output or ""
        self.cu = context_updater

        # cache compiled patterns: key -> compiled regex object or None
        self._pattern_cache: Dict[Tuple[str, int, str], Any] = {}

    # ----------------------- Helpers -----------------------------------------

    def _compile_pattern(self, pattern: str, flags: int = 0, engine: str = "re"):
        """Compile and cache a pattern for the selected engine ('re' or 'regex').
        Returns the compiled pattern or None if compilation failed.
        """
        key = (pattern, flags, engine)
        if key in self._pattern_cache:
            return self._pattern_cache[key]

        try:
            if engine == "regex":
                compiled = regex.compile(pattern, flags)
            else:
                compiled = re.compile(pattern, flags)
        except (re.error, regex.error) as e:
            logger.warning(f"Error compiling matchstring [{pattern}]: {e}")
            self._pattern_cache[key] = None
            return None

        self._pattern_cache[key] = compiled
        return compiled

    def _find_tokens(self, template: str) -> Iterable[int]:
        """Yield integer token indices found in template like $1, $2, ...
        """
        for m in re.finditer(r"\$(\d+)", template):
            yield int(m.group(1))

    def __replace_tokens_from_matchobj(self, template: str, match: re.Match) -> Optional[str]:
        """Replace tokens $N using named groups 'mN' (preferred), falling back to numeric groups.
        """
        output = template
        for idx in sorted(set(self._find_tokens(template))):
            token = f"${{idx}}"
            mname = f"m{idx}"
            # Prefer named group 'mN' if defined in groupdict, else try numeric group
            if mname in match.groupdict():
                val = match.group(mname) or ""
            else:
                try:
                    val = match.group(idx) or ""
                except IndexError:
                    logger.smarterror(
                        f"Invalid matchstring for service={{self.service.name}}, tool={{self.tool_name}}"
                    )
                    return None
            output = output.replace(token, val)
        return output

    def __replace_tokens_from_captdict(self, template: str, captdict: Dict[str, list], index: int) -> Optional[str]:
        """Replace tokens $N using capturesdict from regex.search().capturesdict().
        """
        output = template
        for idx in sorted(set(self._find_tokens(template))):
            token = f"${{idx}}"
            key = f"m{idx}"
            if key in captdict and index < len(captdict[key]):
                val = captdict[key][index] or ""
            else:
                logger.smarterror(
                    f"Invalid matchstring for service={{self.service.name}}, tool={{self.tool_name}}"
                )
                return None
            output = output.replace(token, val)
        return output

    # ----------------------- Detection entry points --------------------------

    def detect_credentials(self) -> None:
        """Detect usernames/credentials from command output.
        Supports two matching methods defined in matchstrings:
         - finditer (default): uses re.finditer and named groups m1... or numeric groups
         - search: uses regex.search and capturesdict() to collect repeated groups
        """
        if self.service.name not in creds_match:
            return

        svc_map = creds_match[self.service.name]
        if self.tool_name not in svc_map:
            return

        p = svc_map[self.tool_name]

        for pattern, spec in p.items():
            logger.debug(f"Search for creds pattern: {{pattern}}")

            if "user" not in spec:
                logger.smarterror(
                    f'Invalid matchstring for service={{self.service.name}}, tool={{self.tool_name}}: Missing "user" key'
                )
                continue

            method = spec.get("meth", "finditer")
            if method not in ("finditer", "search"):
                method = "finditer"

            # perform matching
            try:
                if method == "finditer":
                    compiled = self._compile_pattern(pattern, flags=re.IGNORECASE | re.MULTILINE, engine="re")
                    if not compiled:
                        continue
                    matches = compiled.finditer(self.cmd_output)
                else:  # method == "search"
                    compiled = self._compile_pattern(pattern, flags=regex.IGNORECASE, engine="regex")
                    if not compiled:
                        continue
                    m = compiled.search(self.cmd_output)
                    matches = [m] if m else []
            except (re.error, regex.error) as e:
                logger.warning(f"Error with matchstring [{pattern}], you should review it. Exception: {e}")
                break

            pattern_matched = False

            # finditer: iterate re.Match objects
            if method == "finditer":
                for match in matches:
                    pattern_matched = True
                    user = self.__replace_tokens_from_matchobj(spec["user"], match)
                    if user is None:
                        continue

                    cred_pass = None
                    auth_type = None
                    if "pass" in spec:
                        cred_pass = self.__replace_tokens_from_matchobj(spec["pass"], match)
                        if cred_pass is None:
                            continue
                    if "type" in spec:
                        auth_type = self.__replace_tokens_from_matchobj(spec["type"], match)
                        if auth_type is None:
                            continue

                    if cred_pass is not None:
                        self.cu.add_credentials(username=user, password=cred_pass, auth_type=auth_type)
                    else:
                        self.cu.add_username(username=user, auth_type=auth_type)

            # search: use regex capturesdict()
            else:
                # matches is a list with a single regex.Match or empty
                if not matches:
                    continue

                m = matches[0]
                captdict = m.capturesdict()
                if "m1" not in captdict:
                    logger.smarterror(
                        f'Invalid matchstring for service={{self.service.name}}, tool={{self.tool_name}}: Missing match group'
                    )
                    return

                nb_groups = len(captdict["m1"])
                for i in range(nb_groups):
                    pattern_matched = True
                    user = self.__replace_tokens_from_captdict(spec["user"], captdict, i)
                    if user is None:
                        continue

                    cred_pass = None
                    auth_type = None
                    if "pass" in spec:
                        cred_pass = self.__replace_tokens_from_captdict(spec["pass"], captdict, i)
                        if cred_pass is None:
                            continue
                    if "type" in spec:
                        auth_type = self.__replace_tokens_from_captdict(spec["type"], captdict, i)
                        if auth_type is None:
                            continue

                    if cred_pass is not None:
                        self.cu.add_credentials(username=user, password=cred_pass, auth_type=auth_type)
                    else:
                        self.cu.add_username(username=user, auth_type=auth_type)

            if pattern_matched:
                logger.debug("Creds pattern matches (user only)")
                return

    # ------------------------------------------------------------------------------------

    def detect_specific_options(self) -> None:
        """Detect specific option updates from command output."""
        if self.service.name not in options_match:
            return

        svc_map = options_match[self.service.name]
        if self.tool_name not in svc_map:
            return

        p = svc_map[self.tool_name]

        for pattern, spec in p.items():
            logger.debug(f"Search for option pattern: {{pattern}}")

            try:
                compiled = self._compile_pattern(pattern, flags=re.IGNORECASE | re.MULTILINE, engine="re")
                if not compiled:
                    continue
                m = compiled.search(self.cmd_output)
            except (re.error, regex.error) as e:
                logger.warning(f"Error with matchstring [{pattern}], you should review it. Exception: {e}")
                break

            if not m:
                continue

            logger.debug("Option pattern matches")
            if "name" not in spec:
                logger.smarterror(
                    f'Invalid matchstring for service={{self.service.name}}, tool={{self.tool_name}}: Missing "name" key'
                )
                continue

            name = self.__replace_tokens_from_matchobj(spec["name"], m)
            if name is None:
                continue

            if "value" not in spec:
                logger.smarterror(
                    f'Invalid matchstring for service={{self.service.name}}, tool={{self.tool_name}}: Missing "value" key'
                )
                continue

            value = self.__replace_tokens_from_matchobj(spec["value"], m)
            if value is None:
                continue

            self.cu.add_option(name, value)

    # ------------------------------------------------------------------------------------

    def detect_products(self) -> None:
        """
        Detect product from command output.
        For a given tool/product, first successful match stops further checks for that product type.
        """
        if self.service.name not in products_match:
            return

        for prodtype, proddict in products_match[self.service.name].items():
            break_prodnames = False

            for prodname, prodinfo in proddict.items():
                if self.tool_name not in prodinfo:
                    continue

                patterns = prodinfo[self.tool_name]
                if isinstance(patterns, str):
                    patterns = [patterns]

                for pattern in patterns:
                    version_detection = "[VERSION]" in pattern
                    pattern_re = pattern.replace("[VERSION]", VERSION_REGEXP)
                    logger.debug(f"Search for products pattern: {{pattern_re}}")

                    try:
                        compiled = self._compile_pattern(pattern_re, flags=re.IGNORECASE | re.MULTILINE, engine="re")
                        if not compiled:
                            continue
                        m = compiled.search(self.cmd_output)
                    except (re.error, regex.error) as e:
                        logger.warning(
                            f"Error with matchstring [{pattern_re}], you should review it. Exception: {e}"
                        )
                        break

                    if not m:
                        continue

                    logger.debug("Product pattern matches")
                    version = ""
                    if version_detection:
                        try:
                            version = m.group("version") or ""
                            logger.debug(f"Version detected: {{version}}")
                        except (IndexError, KeyError):
                            version = ""

                    self.cu.add_product(prodtype, prodname, version)

                    # Found a product name for this product type; stop checking other product names
                    break_prodnames = True
                    if version != "":
                        # If version is found we can stop checking patterns for this prodname group
                        break

                if break_prodnames:
                    break

    # ------------------------------------------------------------------------------------

    def detect_vulns(self) -> None:
        """
        Detect vulnerabilities from command output. Multiple occurrences are supported.
        """
        if self.service.name not in vulns_match:
            return

        svc_map = vulns_match[self.service.name]
        if self.tool_name not in svc_map:
            return

        p = svc_map[self.tool_name]

        for pattern, spec in p.items():
            logger.debug(f"Search for vulns pattern: {{pattern}}")

            try:
                compiled = self._compile_pattern(pattern, flags=re.IGNORECASE | re.MULTILINE, engine="re")
                if not compiled:
                    continue
                mall = compiled.finditer(self.cmd_output)
            except (re.error, regex.error) as e:
                logger.warning(f"Error with matchstring [{pattern}], you should review it. Exception: {e}")
                break

            if not mall:
                continue

            for m in mall:
                name = self.__replace_tokens_from_matchobj(spec, m)
                if name is None:
                    continue
                logger.debug("Vuln pattern matches")
                self.cu.add_vuln(StringUtils.remove_non_printable_chars(name))

    # ------------------------------------------------------------------------------------

    def detect_os(self) -> None:
        """
        Detect operating system from command output.
        """
        for os_name, patterns_map in os_match.items():
            if self.tool_name not in patterns_map:
                continue

            patterns = patterns_map[self.tool_name]
            if isinstance(patterns, str):
                patterns = [patterns]

            for pattern in patterns:
                logger.debug(f"Search for os pattern: {{pattern}}")
                try:
                    compiled = self._compile_pattern(pattern, flags=re.IGNORECASE, engine="re")
                    if not compiled:
                        continue
                    m = compiled.search(self.cmd_output)
                except (re.error, regex.error) as e:
                    logger.warning(f"Error with matchstring [{pattern}], you should review it. Exception: {e}")
                    break

                if m:
                    logger.debug("OS pattern matches")
                    self.cu.add_os(os_name)
                    return
        
