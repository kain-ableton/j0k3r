#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path

TARGET = Path("lib/controller/DbController.py")
if not TARGET.exists():
    raise SystemExit("DbController.py not found at lib/controller/DbController.py")

src = TARGET.read_text(encoding="utf-8", errors="ignore")
orig = src

# Ensure from __future__ at top
if "from __future__ import annotations" not in src:
    src = "from __future__ import annotations\n" + src

# Insert cmd2 fallback shim after import block
shim = """
try:
    import cmd2  # type: ignore
    BaseCmd = cmd2.Cmd
    HAVE_CMD2 = True
except Exception:  # pragma: no cover
    import cmd
    BaseCmd = cmd.Cmd
    HAVE_CMD2 = False
""".strip()+"\n"

m = re.search(r"^(?:from[^\n]*\n|import[^\n]*\n)+", src, flags=re.M)
pos = m.end() if m else 0
if "HAVE_CMD2" not in src:
    src = src[:pos] + ("\n" if pos else "") + shim + src[pos:]

# Force class to inherit from BaseCmd
src = re.sub(r"^(\s*class\s+DbController\s*\()([^)]*)(\)\s*:)", r"\1BaseCmd\3", src, flags=re.M)

# Sanitize __init__: remove cmd2-only kwargs and call super().__init__() tolerant
# Replace any 'super().__init__(...use_ipython... )' or any kwargs with plain calls, wrapped try/except
src = re.sub(
    r"(def\s+__init__\s*\(self[\s\S]*?\):\s*\n)(\s*)super\(\)\.__init__\([^\)]*\)",
    r"\1\2# tolerant init for cmd/cmd2\n\2try:\n\2    super().__init__()\n\2except TypeError:\n\2    super().__init__()",
    src, flags=re.M
)
# If we didn't match, ensure at least one tolerant call exists
if "tolerant init for cmd/cmd2" not in src:
    src = re.sub(
        r"(def\s+__init__\s*\(self[\s\S]*?\):\s*\n)(\s*)super\(\)\.__init__\(\)",
        r"\1\2# tolerant init for cmd/cmd2\n\2try:\n\2    super().__init__()\n\2except TypeError:\n\2    super().__init__()",
        src, flags=re.M
    )

# On startup, enable some cmd2 niceties if available
if "HAVE_CMD2" in src and "if HAVE_CMD2:" not in src:
    src = re.sub(
        r"(def\s+__init__\s*\(self[\s\S]*?\):\s*\n[\s\S]*?tolerant init for cmd/cmd2[\s\S]*?\n)",
        r"\1        if HAVE_CMD2:\n            try:\n                self.allow_cli_args = False\n                self.intro = getattr(self, 'intro', 'DB console ready')\n                self.default_to_shell = False\n                # persistent history in settings/\n                self.hist_file = 'settings/.dbconsole_history'\n            except Exception:\n                pass\n",
        src, flags=re.M
    )

# Replace any direct 'import cmd as cmd' or 'class DbController(cmd.Cmd)' leftovers
src = re.sub(r"^\s*import\s+cmd\s*$", "import cmd", src, flags=re.M)
src = re.sub(r"\bcmd\.Cmd\b", "BaseCmd", src)

if src != orig:
    TARGET.write_text(src, encoding="utf-8")
    print("[*] DbController migrated to cmd2-compatible base (with fallback).")
else:
    print("[*] No changes applied; file already migrated.")
