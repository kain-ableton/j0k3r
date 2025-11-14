# Jok3r: cmd2 migration + product registry seeds

## Apply
```bash
unzip -o jok3r_cmd2_migration_pack.zip -d /home/k/projects/jok3r
cd /home/k/projects/jok3r
python3 scripts/migrate_to_cmd2.py
python3 scripts/update_requirements_cmd2.py
```

## Install deps
```bash
. .venv/bin/activate 2>/dev/null || python3 -m venv .venv && . .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

## Preflight + DB init
```bash
PYTHONPATH=. python3 scripts/preflight_contexts.py --root . || true
python3 - <<'PY'
from lib.db import create_all, get_session
create_all()
s = get_session(); s.close()
print("DB ready")
PY
```

## Run
```bash
python3 jok3r.py db   # now uses cmd2 shell if available
python3 run_modern.py attack -t https://pentest-ground.com:4280 -s http --fast --modern-runner --modern-max-concurrent 8
```

## Notes
- The DB console inherits from `cmd2.Cmd` when installed; falls back to stdlib `cmd.Cmd` otherwise.
- Extra product registries added: AJP, SMTP, MSSQL, Oracle, including useful bucket aliases (e.g., `web-appserver`).
