#!/usr/bin/env bash
# Install tools for a specific service
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${SCRIPT_DIR}/.env/bin/python3"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <service>"
    echo ""
    echo "Available services:"
    "${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" info --services 2>/dev/null | grep -E "^\| [a-z]" | awk '{print "  - " $2}'
    exit 1
fi

SERVICE="$1"

cd "${SCRIPT_DIR}"

if [ ! -x "${VENV_PYTHON}" ]; then
    echo "[!] Virtual environment not found. Run ./update.sh first." >&2
    exit 1
fi

echo "[*] Installing tools for service: ${SERVICE}..."
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --install "${SERVICE}" --auto

echo "[*] Installation complete!"
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --show "${SERVICE}"
