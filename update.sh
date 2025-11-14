#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

print_info() {
    BOLD_BLUE=$(tput bold ; tput setaf 4)
    NORMAL=$(tput sgr0)
    echo "${BOLD_BLUE}$1${NORMAL}"
}

print_success() {
    BOLD_GREEN=$(tput bold ; tput setaf 2)
    NORMAL=$(tput sgr0)
    echo "${BOLD_GREEN}$1${NORMAL}"
}

print_error() {
    BOLD_RED=$(tput bold ; tput setaf 1)
    NORMAL=$(tput sgr0)
    echo "${BOLD_RED}$1${NORMAL}" >&2
}

print_warning() {
    BOLD_YELLOW=$(tput bold ; tput setaf 3)
    NORMAL=$(tput sgr0)
    echo "${BOLD_YELLOW}$1${NORMAL}"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${SCRIPT_DIR}/.venv/bin/python"

clear
cd "${SCRIPT_DIR}"

print_info "[~] Pulling latest changes from git..."
git pull
if [ $? -ne 0 ]; then
    print_error "[!] Git pull failed"
    exit 1
fi

print_info "[~] Running dependencies install script..."
"${SCRIPT_DIR}/install-dependencies.sh"
if [ $? -ne 0 ]; then
    print_error "[!] Dependencies install failed"
    exit 1
fi

if [ ! -x "${VENV_PYTHON}" ]; then
    print_error "[!] Jok3r virtual environment is missing at ${VENV_PYTHON}"
    exit 1
fi

print_info "[~] Updating all tools in toolbox..."
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --update-all --fast
if [ $? -ne 0 ]; then
    print_warning "[!] Some tools failed to update (check logs above)"
fi

print_info "[~] Installing/updating all tools in toolbox..."
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --install-all --fast
if [ $? -ne 0 ]; then
    print_warning "[!] Some tools failed to install (check logs above)"
fi

print_info "[~] Showing toolbox content..."
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --show-all

print_success "[+] Update completed successfully"
