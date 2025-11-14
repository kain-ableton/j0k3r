#!/usr/bin/env bash
# Quick update script - only updates already installed tools
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${SCRIPT_DIR}/.env/bin/python3"

cd "${SCRIPT_DIR}"

if [ ! -x "${VENV_PYTHON}" ]; then
    echo "[!] Virtual environment not found. Run ./update.sh first." >&2
    exit 1
fi

echo "[*] Updating all installed tools..."
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --update-all --auto

echo "[*] Update complete!"
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --show-all | grep "OK |"
