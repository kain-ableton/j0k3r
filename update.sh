#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${SCRIPT_DIR}/.venv/bin/python"

clear
cd "${SCRIPT_DIR}"

git pull
"${SCRIPT_DIR}/install-dependencies.sh"

if [ ! -x "${VENV_PYTHON}" ]; then
    echo "[!] Jok3r virtual environment is missing at ${VENV_PYTHON}" >&2
    exit 1
fi

"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --update-all --fast
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --install-all --fast
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --show-all
