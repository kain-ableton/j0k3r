#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

print_green() {
    BOLD_GREEN=$(tput bold ; tput setaf 2)
    NORMAL=$(tput sgr0)
    echo "${BOLD_GREEN}$1${NORMAL}"
}

print_yellow() {
    BOLD_YELLOW=$(tput bold ; tput setaf 3)
    NORMAL=$(tput sgr0)
    echo "${BOLD_YELLOW}$1${NORMAL}"
}

print_red() {
    BOLD_YELLOW=$(tput bold ; tput setaf 1)
    NORMAL=$(tput sgr0)
    echo "${BOLD_YELLOW}$1${NORMAL}"
}

print_blue() {
    BOLD_YELLOW=$(tput bold ; tput setaf 4)
    NORMAL=$(tput sgr0)
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
print_blue "=============================="
print_blue " Jok3r - Installation Script  "
print_blue "=============================="
echo
echo

# Make sure we are root !
if [ "$EUID" -ne 0 ]; then 
    print_red "[!] Must be run as root"
    exit 1
fi

# -----------------------------------------------------------------------------

print_blue "[~] Running dependencies install script..."
"${SCRIPT_DIR}/install-dependencies.sh"
if [ $? -eq 0 ]; then
    print_green "[+] Dependencies install script exited with success returncode"
else
    print_red "[!] Dependencies install script exited with error returncode"
    exit 1
fi

if [ ! -x "${VENV_PYTHON}" ]; then
    print_red "[!] Jok3r virtual environment is missing at ${VENV_PYTHON}"
    exit 1
fi
print_delimiter

# -----------------------------------------------------------------------------

print_blue "[~] Running Jok3r full toolbox install (in non-interactive mode)..."
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --install-all --auto
if [ $? -eq 0 ]; then
    print_green "[+] Jok3r toolbox install exited with success returncode"
else
    print_red "[!] Jok3r toolbox install exited with error returncode"
    exit 1
fi
print_delimiter

# -----------------------------------------------------------------------------

print_blue "[~] Running automatic check of all installed tools (based on returncodes)..."
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --check
if [ $? -eq 0 ]; then
    print_green "[+] Toolbox automatic check exited with success returncode"
else
    print_red "[!] Toolbox automatic check exited with error returncode"
    exit 1
fi
print_delimiter

# -----------------------------------------------------------------------------

print_blue "[~] Print toolbox content"
"${VENV_PYTHON}" "${SCRIPT_DIR}/jok3r.py" toolbox --show-all

# -----------------------------------------------------------------------------

print_green "[+] Install script finished with success"
