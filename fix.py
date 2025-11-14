cd /home/k/projects/j0k3r

python3 - <<'PY'
from pathlib import Path
import re, py_compile

p = Path("lib/controller/DbController.py")
s = p.read_text(encoding="utf-8")
lines = s.splitlines(True)

def next_nonblank_idx(lines, start):
    j = start
    while j < len(lines) and re.match(r'^\s*(#.*)?\n?$', lines[j]):
        j += 1
    return j

insertions = 0
i = 0
while i < len(lines):
    m = re.match(r'^(\s*)except\b[^:]*:\s*(?:#.*)?\n?$', lines[i])
    if m:
        base = m.group(1)
        j = next_nonblank_idx(lines, i+1)
        needs_body = (j >= len(lines)) or not lines[j].startswith(base + "    ")
        if needs_body:
            lines.insert(i+1, f"{base}    pass\n")
            insertions += 1
            i += 1
    i += 1

new_s = "".join(lines)
if new_s != s:
    p.write_text(new_s, encoding="utf-8")

# quick compile check for this file
py_compile.compile(str(p), doraise=True)
print(f"Fixed bare except blocks inserted: {insertions}")
PY
