#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Color definitions
BOLD_BLUE=$(tput bold ; tput setaf 4)
BOLD_GREEN=$(tput bold ; tput setaf 2)
BOLD_RED=$(tput bold ; tput setaf 1)
BOLD_YELLOW=$(tput bold ; tput setaf 3)
NORMAL=$(tput sgr0)

print_info() {
    echo "${BOLD_BLUE}$1${NORMAL}"
}

print_success() {
    echo "${BOLD_GREEN}$1${NORMAL}"
}

print_error() {
    echo "${BOLD_RED}$1${NORMAL}" >&2
}

print_warning() {
    echo "${BOLD_YELLOW}$1${NORMAL}"
}

print_delimiter() {
    echo
    echo "-------------------------------------------------------------------------------"
    echo
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${SCRIPT_DIR}/.venv/bin/python"

cd "${SCRIPT_DIR}"

echo
echo
print_info "=============================="
print_info " Jok3r - Installation Script  "
print_info "=============================="
echo
echo

# Make sure we are root !
if [ "$EUID" -ne 0 ]; then 
    print_error "[!] Must be run as root"
    exit 1
fi

# -----------------------------------------------------------------------------

print_info "[~] Running dependencies install script..."
"${SCRIPT_DIR}/install-dependencies.sh"
if [ $? -eq 0 ]; then
    print_success "[+] Dependencies install script exited with success returncode"
else
    print_error "[!] Dependencies install script exited with error returncode"
    exit 1
fi

if [ ! -x "${VENV_PYTHON}" ]; then
    print_error "[!] Jok3r virtual environment is missing at ${VENV_PYTHON}"
    exit 1
fi
print_delimiter

# -----------------------------------------------------------------------------

print_info "[~] Running Jok3r full toolbox install (in non-interactive mode)..."
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --install-all --auto
if [ $? -eq 0 ]; then
    print_success "[+] Jok3r toolbox install exited with success returncode"
else
    print_error "[!] Jok3r toolbox install exited with error returncode"
    exit 1
fi
print_delimiter

# -----------------------------------------------------------------------------

print_info "[~] Running automatic check of all installed tools (based on returncodes)..."
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --check
if [ $? -eq 0 ]; then
    print_success "[+] Toolbox automatic check exited with success returncode"
else
    print_error "[!] Toolbox automatic check exited with error returncode"
    exit 1
fi
print_delimiter

# -----------------------------------------------------------------------------

print_info "[~] Print toolbox content"
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --show-all

# -----------------------------------------------------------------------------

print_success "[+] Install script finished with success"
