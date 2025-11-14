#!/usr/bin/env bash
# Jok3r - Simplified installer for Kali Linux 2025.3+
# Uses an existing .env virtualenv if present and assumes SQLite as DB backend.

set -euo pipefail

# -----------------------------
# Helpers
# -----------------------------
COLOR_RED="\033[1;31m"
COLOR_GREEN="\033[1;32m"
COLOR_BLUE="\033[1;34m"
COLOR_RESET="\033[0m"

print_red()   { printf "${COLOR_RED}%s${COLOR_RESET}\n"   "$*"; }
print_green() { printf "${COLOR_GREEN}%s${COLOR_RESET}\n" "$*"; }
print_blue()  { printf "${COLOR_BLUE}%s${COLOR_RESET}\n"  "$*"; }

require_root() {
    if [ "$(id -u)" -ne 0 ]; then
        print_red "[!] This script must be run as root (use sudo)."
        exit 1
    fi
}

# -----------------------------
# OS detection (Kali only)
# -----------------------------
check_os() {
    if [ -r /etc/os-release ]; then
        . /etc/os-release
        if [ "${ID:-}" != "kali" ] && [[ "${ID_LIKE:-}" != *"kali"* ]]; then
            print_red "[!] This installer is intended for Kali Linux only."
            print_red "    Detected: ID=${ID:-unknown}, ID_LIKE=${ID_LIKE:-unknown}"
            exit 1
        fi
    else
        print_red "[!] Cannot detect OS (no /etc/os-release). Abort."
        exit 1
    fi
    print_green "[+] Kali Linux detected."
}

# -----------------------------
# APT operations
# -----------------------------
apt_update() {
    print_blue "[~] Updating APT repositories..."
    apt update -y
    print_green "[+] APT repositories updated."
}

install_packages() {
    print_blue "[~] Installing required system packages (if missing)..."

    BASE_PACKAGES="
        git
        curl
        wget
        ca-certificates
        build-essential
        pkg-config
    "

    TOOLS_PACKAGES="
        metasploit-framework
        nmap
        tcpdump
    "

    PY_PACKAGES="
        python3
        python3-pip
        python3-dev
        python3-setuptools
        python3-venv
        python3-wheel
        python3-psycopg2
        python3-pymysql
        python3-shodan
    "

    LIB_PACKAGES="
        libpq-dev
        libffi-dev
        libssl-dev
        sqlite3
    "

    ALL_PACKAGES="
        ${BASE_PACKAGES}
        ${TOOLS_PACKAGES}
        ${PY_PACKAGES}
        ${LIB_PACKAGES}
    "

    for pkg in ${ALL_PACKAGES}; do
        if ! dpkg -s "$pkg" >/dev/null 2>&1; then
            print_blue "[~] Installing ${pkg}..."
            DEBIAN_FRONTEND=noninteractive apt install -y "$pkg"
        else
            print_green "[+] ${pkg} already installed."
        fi
    done

    print_green "[+] All required system packages are installed."
}

# -----------------------------
# Python virtual environment (.env)
# -----------------------------
create_or_use_env() {
    print_blue "[~] Setting up Python virtual environment (.env)..."

    if ! command -v python3 >/dev/null 2>&1; then
        print_red "[!] python3 not found even after package installation."
        exit 1
    fi

    if [ -d ".env" ]; then
        print_green "[+] Existing virtual environment .env detected. Reusing it."
    else
        print_blue "[~] Creating new virtual environment at .env"
        python3 -m venv .env
    fi

    # shellcheck disable=SC1091
    . .env/bin/activate

    print_blue "[~] Upgrading pip, setuptools, and wheel inside .env..."
    pip install --upgrade pip setuptools wheel

    print_green "[+] Virtual environment .env is ready."
}

# -----------------------------
# Python dependencies (Jok3r)
# -----------------------------
install_python_deps() {
    # shellcheck disable=SC1091
    . .env/bin/activate

    if [ -f "requirements.txt" ]; then
        print_blue "[~] Installing Python dependencies from requirements.txt..."
        pip install -r requirements.txt
        print_green "[+] Python dependencies installed from requirements.txt."
    elif [ -f "requirements-kali.txt" ]; then
        print_blue "[~] Installing Python dependencies from requirements-kali.txt..."
        pip install -r requirements-kali.txt
        print_green "[+] Python dependencies installed from requirements-kali.txt."
    else
        print_blue "[~] No requirements.txt or requirements-kali.txt found."
        print_blue "    Install any extra Python packages manually inside .env if required."
    fi
}

# -----------------------------
# Jok3r basic check
# -----------------------------
final_check() {
    # shellcheck disable=SC1091
    . .env/bin/activate

    print_blue "[~] Verifying Jok3r basic CLI..."

    if [ -f "run_modern.py" ]; then
        print_blue "[~] Found run_modern.py, checking that it starts..."
        python run_modern.py --help >/dev/null 2>&1 || true
    fi

    if [ -f "jok3r.py" ]; then
        print_blue "[~] Found jok3r.py, checking that it starts..."
        python jok3r.py --help >/dev/null 2>&1 || true
    fi

    print_green "[+] Installation steps completed."
    print_blue  "[~] To use Jok3r with SQLite and .env, run:"
    echo
    echo "    cd \"$(pwd)\""
    echo "    source .env/bin/activate"
    echo "    python run_modern.py --help"
    echo
}

# -----------------------------
# Main
# -----------------------------
main() {
    require_root
    print_blue "=============================="
    print_blue " Jok3r - Kali 2025.3 Installer"
    print_blue "  (.env + SQLite backend)     "
    print_blue "=============================="
    echo

    check_os
    apt_update
    install_packages
    create_or_use_env
    install_python_deps
    final_check
}

main "$@"
