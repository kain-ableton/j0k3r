#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path

pins = [
    "cmd2>=2.4,<3.0",
    "pyperclip>=1.8",
    "wcwidth>=0.2",
]

paths = [Path("requirements.txt"), Path("requirements.in")]
modified = False
for p in paths:
    if not p.exists(): 
        continue
    txt = p.read_text(encoding="utf-8", errors="ignore")
    before = txt
    for pin in pins:
        if pin not in txt:
            txt = txt.rstrip() + "\n" + pin + "\n"
    if txt != before:
        p.write_text(txt, encoding="utf-8")
        modified = True
        print(f"[*] updated {p}")
if not modified:
    t = Path("requirements.txt")
    if not t.exists():
        t.write_text("\n".join(pins) + "\n", encoding="utf-8")
        print("[*] created requirements.txt with cmd2 pins")
    else:
        print("[*] requirements already contained pins")
