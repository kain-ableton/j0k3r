#!/usr/bin/env python3
"""
Check Jok3r toolbox tool availability by running each check_command.

Default config path: ./toolbox.conf (override with -c).
"""

import argparse
import configparser
import subprocess
import shlex
from pathlib import Path
from typing import List, Tuple


def load_config(path: Path) -> configparser.ConfigParser:
    if not path.is_file():
        raise SystemExit(f"[!] Config file not found: {path}")
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.read(path)
    return cfg


def run_check(tool: str, cmd: str, timeout: int = 15) -> Tuple[bool, int, str]:
    """Run a check_command via /bin/sh and return (ok, rc, short_output)."""
    if not cmd.strip():
        return False, 0, "no check_command"

    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            text=True,
        )
        ok = proc.returncode == 0
        # keep output short to avoid spam
        out = (proc.stdout or "").strip()
        if len(out) > 400:
            out = out[:400] + "... [truncated]"
        return ok, proc.returncode, out
    except subprocess.TimeoutExpired:
        return False, -1, f"timeout after {timeout}s"
    except Exception as exc:
        return False, -2, f"exception: {exc}"


def iter_tools(cfg: configparser.ConfigParser) -> List[Tuple[str, str, str]]:
    tools = []
    for section in cfg.sections():
        # Skip non-tool sections if you have any; here we assume every section is a tool.
        name = cfg.get(section, "name", fallback=section)
        check_cmd = cfg.get(section, "check_command", fallback="").strip()
        tools.append((section, name, check_cmd))
    return tools


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Check Jok3r toolbox tool availability using check_command."
    )
    ap.add_argument(
        "-c",
        "--config",
        default="toolbox.conf",
        help="Path to toolbox.conf (default: %(default)s)",
    )
    ap.add_argument(
        "--show-output",
        action="store_true",
        help="Show truncated command output even on success.",
    )
    ap.add_argument(
        "--filter",
        metavar="SUBSTR",
        help="Only test tools whose section OR name contains this substring (case-insensitive).",
    )
    args = ap.parse_args()

    cfg_path = Path(args.config)
    cfg = load_config(cfg_path)

    tools = iter_tools(cfg)
    if args.filter:
        f = args.filter.lower()
        tools = [
            (sec, name, cmd)
            for sec, name, cmd in tools
            if f in sec.lower() or f in name.lower()
        ]

    print(f"[+] Loaded {len(tools)} tool sections from {cfg_path}")
    ok_count = 0
    fail_count = 0
    skip_count = 0

    for section, name, cmd in tools:
        label = f"{section} ({name})"
        if not cmd:
            print(f"[-] {label}: SKIP (no check_command)")
            skip_count += 1
            continue

        print(f"[~] Checking {label}")
        ok, rc, out = run_check(section, cmd)

        if ok:
            ok_count += 1
            line = f"[+] {label}: OK (rc={rc})"
        else:
            fail_count += 1
            line = f"[!] {label}: FAIL (rc={rc})"

        print(line)
        if args.show_output or not ok:
            if out:
                print(f"    Output:\n        " + "\n        ".join(out.splitlines()))
            else:
                print("    Output: <empty>")

    print()
    print(f"[=] Summary: OK={ok_count}  FAIL={fail_count}  SKIP={skip_count}")


if __name__ == "__main__":
    main()
