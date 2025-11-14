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
VENV_DIR="${SCRIPT_DIR}/.venv"
VENV_PYTHON="${VENV_DIR}/bin/python"
VENV_PIP="${VENV_DIR}/bin/pip"

echo
echo
print_info "=============================="
print_info " Jok3r - Dependencies Install "
print_info "=============================="
echo
echo
print_info "This script will install Jok3r and all the required dependencies"

# Make sure we are root !
if [ "$EUID" -ne 0 ]; then 
    print_error "[!] Must be run as root"
    exit 1
fi

# Make sure we are on Debian-based OS
OS=`(lsb_release -sd || grep NAME /etc/*-release) 2> /dev/null`
print_info "[~] Detected OS:"
echo $OS
if echo "$OS" | egrep -iq '(kali|debian|ubuntu)'; then
    print_success "[+] Debian-based Linux OS detected !"
else
    print_error "[!] No Debian-based Linux OS detected (Debian/Ubuntu/Kali). Will not be able to continue !"
    exit 1
fi
echo
echo

# -----------------------------------------------------------------------------
# Verify Python3 availability (required for Kali 2025 environments)

if ! command -v python3 >/dev/null 2>&1; then
    print_error "[!] Python3 is required but not installed"
    exit 1
fi

# -----------------------------------------------------------------------------
# Prepare Python virtual environment for Jok3r dependencies

if ! dpkg-query -W -f='${Status}' python3-venv 2>/dev/null | grep -q "ok installed"; then
    print_info "[~] Installing python3-venv package required for virtual environments"
    apt-get update
    apt-get install -y python3-venv
    if ! dpkg-query -W -f='${Status}' python3-venv 2>/dev/null | grep -q "ok installed"; then
        print_error "[!] Failed to install python3-venv"
        exit 1
    fi
fi

if [ ! -d "${VENV_DIR}" ]; then
    print_info "[~] Creating Jok3r Python virtual environment at ${VENV_DIR}"
    python3 -m venv "${VENV_DIR}"
    if [ $? -ne 0 ]; then
        print_error "[!] Failed to create Jok3r virtual environment"
        exit 1
    fi
else
    print_success "[+] Jok3r Python virtual environment already exists"
fi

if [ ! -x "${VENV_PYTHON}" ]; then
    print_error "[!] Jok3r virtual environment is missing the python binary"
    exit 1
fi

print_info "[~] Upgrading pip inside Jok3r virtual environment"
"${VENV_PYTHON}" -m pip install --upgrade pip
if [ $? -ne 0 ]; then
    print_error "[!] Failed to upgrade pip inside the Jok3r virtual environment"
    exit 1
fi

if [ ! -x "${VENV_PIP}" ]; then
    print_error "[!] pip not found inside the Jok3r virtual environment"
    exit 1
fi

print_delimiter

# -----------------------------------------------------------------------------
# Add Kali repositories if not on Kali (Debian/Ubuntu)

if ! grep -q "deb http://http.kali.org/kali kali-rolling main" /etc/apt/sources.list; then
    print_info "[~] Add Kali repository (because missing in /etc/apt/sources.list)"
    cp /etc/apt/sources.list /etc/apt/sources.list.bak
    echo "deb http://http.kali.org/kali kali-rolling main non-free contrib" >> /etc/apt/sources.list
    cd /tmp/
    wget -k https://http.kali.org/kali/pool/main/k/kali-archive-keyring/kali-archive-keyring_2018.1_all.deb
    dpkg -i kali-archive-keyring_2018.1_all.deb
    rm -f kali-archive-keyring_2018.1_all.deb
    apt-get update
    apt-get install -y kali-archive-keyring
    if [ $? -eq 0 ]; then
        print_success "[+] Kali repository added with success"
    else
        print_error "[!] Error occurred while adding Kali repository"
        exit 1
    fi
else
    print_info "[~] Kali repository detected in /etc/apt/sources.list. Updating repositories..."
    apt-get update
    if [ $? -eq 0 ]; then
        print_success "[+] Repositories updated with success"
    else
        print_error "[!] Error occurred while updating repositories"
        exit 1
    fi
fi
print_delimiter

# -----------------------------------------------------------------------------
# Install Git

if ! command -v git >/dev/null 2>&1; then
    print_info "[~] Install git ..."
    apt-get install -y git
    if command -v git >/dev/null 2>&1; then
        print_success "[+] Git installed successfully"
    else
        print_error "[!] An error occurred during Git install"
        exit 1
    fi
else
    print_success "[+] Git is already installed"
fi
print_delimiter

# -----------------------------------------------------------------------------
# Install various required packages 

print_info "[~] Install various required packages (if missing)"

PACKAGES="
alien
apt-transport-https
apt-utils
automake
bc
build-essential
curl
dnsutils
gawk
gcc
gnupg2
iputils-ping
libcurl4-openssl-dev
libffi-dev
libgmp-dev
liblzma-dev
libpq-dev
libssl-dev
libwhisker2-perl
libwww-perl
libxml2
libxml2-dev
libxml2-utils
libxslt1-dev
locales
locate
make
net-tools
patch
postgresql
postgresql-contrib
procps
smbclient
sudo
unixodbc
unixodbc-dev
unzip
wget
zlib1g-dev
"
for package in $PACKAGES; do
    if ! dpkg-query -W -f='${Status}' "$package" 2>/dev/null | grep -q "ok installed"; then
        echo
        print_info "[~] Install ${package} ..."
        apt-get install -y "$package"
    fi
done
print_delimiter

# -----------------------------------------------------------------------------
# Install Metasploit-framework

if ! command -v msfconsole >/dev/null 2>&1; then
    print_info "[~] Install Metasploit ..."
    apt-get install -y metasploit-framework 
    if command -v msfconsole >/dev/null 2>&1; then
        print_success "[+] Metasploit installed successfully"
    else
        print_error "[!] An error occurred during Metasploit install"
        exit 1
    fi        
else
    print_success "[+] Metasploit is already installed"
fi
print_delimiter

# -----------------------------------------------------------------------------
# Install Nmap 

if ! command -v nmap >/dev/null 2>&1; then
    print_info "[~] Install Nmap ..."
    apt-get install -y nmap 
    if command -v nmap >/dev/null 2>&1; then
        print_success "[+] Nmap installed successfully"
    else
        print_error "[!] An error occurred during Nmap install"
        exit 1
    fi   
else
    print_success "[+] Nmap is already installed"
fi
print_delimiter

# -----------------------------------------------------------------------------
# Install Tcpdump

if ! command -v tcpdump >/dev/null 2>&1; then
    print_info "[~] Install tcpdump ..."
    apt-get install -y tcpdump
    if command -v tcpdump >/dev/null 2>&1; then
        print_success "[+] tcpdump installed successfully"
    else
        print_error "[!] An error occurred during tcpdump install"
        exit 1
    fi   
else
    print_success "[+] tcpdump is already installed"
fi
print_delimiter

# -----------------------------------------------------------------------------

# if ! command -v npm >/dev/null 2>&1; then
#     print_success "[~] Install NodeJS ..."
#     curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
#     apt-get install -y nodejs
# else
#     print_success "[+] NodeJS is already installed"
# fi
# print_delimiter   

# -----------------------------------------------------------------------------
# Install Python and related packages
print_info "[~] Install Python 3 and useful related packages (if missing)"

PACKAGES="
python3
python3-pip
python3-dev
python3-setuptools
python3-distutils
python3-venv
python3-wheel
python3-psycopg2
python3-pymysql
python3-shodan
"

for package in $PACKAGES; do
    if ! dpkg-query -W -f='${Status}' "$package" 2>/dev/null | grep -q "ok installed"; then
        echo
        print_info "[~] Install ${package} ..."
        apt-get install -y "$package"
    fi
done

if command -v python3 >/dev/null 2>&1; then
    print_success "[+] Python3 installed successfully"
else
    print_error "[!] An error occurred during Python3 install"
    exit 1
fi
if command -v pip3 >/dev/null 2>&1; then
    print_success "[+] pip3 installed successfully"
else
    print_error "[!] An error occurred during pip3 install"
    exit 1
fi
print_delimiter

# -----------------------------------------------------------------------------
# Install Python virtualenv

print_info "[~] Python3 virtual environments handled via built-in venv module"
if command -v virtualenv >/dev/null 2>&1; then
    print_success "[+] Legacy virtualenv command already installed"
else
    print_info "[~] Skipping virtualenv (python3 -m venv will be used)"
fi
print_delimiter

# -----------------------------------------------------------------------------
# Install common Python libraries
# We decide to add system-wide install of common Python libraries even if
# most of Python tools are then installed inside virtualenv, because it appears
# that a lot of projects/tools do not embed correct requirements.txt or
# setup.py. Then virtualenv for Python projects are created with 
# --system-site-package option which allows to access those libraries.

print_info "[~] Install common Python libraries..."

LIBPY3="
aiohttp
ansi2html
argcomplete
asn1crypto
async-timeout
asyncio
attrs
Babel
bcrypt
beautifulsoup4
blessed
bs4
cement
Cerberus
certifi
cffi
chardet
cmd2
colorama
colored
colorlog
configparser
cryptography
cssselect
dnspython
docutils
enlighten
entrypoints
Flask
future
html-similarity
html5lib
humanfriendly
humanize
idna
imagesize
inflect
ipaddress
IPy
ipparser
itsdangerous
keyring
keyrings.alt
ldap3
ldapdomaindump
logutils
lxml
macholib
MarkupSafe
maxminddb
multidict
netaddr
ntlm-auth
packaging
paramiko
parsel
passlib
pbr
Pillow
pluginbase
ply
pockets
prettytable
prompt-toolkit
proxy-db
psycopg2
psycopg2-binary
pyasn1
pycparser
pycryptodomex
pycurl
Pygments
PyGObject
pymongo
pymssql
PyMySQL
PyNaCl
pyodbc
pyOpenSSL
pyparsing
pyperclip
pysmi
pysnmp
PySocks
python-libnmap
python-memcached
python-nmap
pytz
pystache
pyxdg
PyYAML
redis
regex
requests
requests-mock
requests-ntlm
requests-toolbelt
scapy
SecretStorage
selenium
shodan
six
snowballstemmer
soupsieve
Sphinx
sphinx-better-theme
sphinxcontrib-napoleon
sphinxcontrib-websupport
SQLAlchemy
SQLAlchemy-Utils
stem
stevedore
tabulate
termcolor
tld
tqdm
urllib3
veryprettytable
virtualenv
virtualenv-clone
virtualenvwrapper
w3lib
wcwidth
webencodings
Werkzeug
yarl
"

PIP3FREEZE=$("${VENV_PIP}" freeze)
for lib in $LIBPY3; do
    if ! echo "$PIP3FREEZE" | grep -iq "$lib"; then
        echo
        print_blue "[~] Install Python library ${lib} (py3)"
        "${VENV_PIP}" install "$lib"
    fi
done

print_delimiter

# -----------------------------------------------------------------------------
# Install Jython

if ! command -v jython >/dev/null 2>&1; then
    print_info "[~] Install Jython"
    apt-get install -y jython
    if command -v jython >/dev/null 2>&1; then
        print_success "[+] Jython installed successfully"
    else
        print_error "[!] An error occurred during Jython install"
        exit 1
    fi   
else
    print_success "[+] Jython is already installed"
fi
print_delimiter

# -----------------------------------------------------------------------------
# Install Ruby

if ! command -v ruby >/dev/null 2>&1; then
    print_info "[~] Install Ruby"
    apt-get install -y ruby ruby-dev
    if command -v ruby >/dev/null 2>&1; then
        print_success "[+] Ruby installed successfully"
    else
        print_error "[!] An error occurred during Ruby install"
        exit 1
    fi   
else
    print_success "[+] Ruby is already installed"
fi
print_delimiter

# -----------------------------------------------------------------------------
# Update Ruby bundler (system Ruby)

if command -v gem >/dev/null 2>&1; then
    print_info "[~] Update Ruby bundler"
    gem install bundler
    print_delimiter
fi

# -----------------------------------------------------------------------------
# Install Perl

if ! command -v perl >/dev/null 2>&1; then
    print_info "[~] Install Perl"
    apt-get install -y perl 
    if command -v perl >/dev/null 2>&1; then
        print_success "[+] Perl installed successfully"
    else
        print_error "[!] An error occurred during Perl install"
        exit 1
    fi   
else
    print_success "[+] Perl is already installed"
fi
print_delimiter

# -----------------------------------------------------------------------------
# Install PHP

if ! command -v php >/dev/null 2>&1; then
    print_info "[~] Install PHP"
    apt-get install -y php
    if command -v php >/dev/null 2>&1; then
        print_success "[+] PHP installed successfully"
    else
        print_error "[!] An error occurred during PHP install"
        exit 1
    fi   
else
    print_success "[+] PHP is already installed"
fi
print_delimiter

# -----------------------------------------------------------------------------
# Install Java

if ! command -v java >/dev/null 2>&1; then
    print_info "[~] Install Java"
    apt-get install -y default-jdk
    if command -v java >/dev/null 2>&1; then
        print_green "[+] Java installed successfully"
    else
        print_red "[!] An error occurred during Java install"
        exit 1
    fi   
else
    print_success "[+] Java is already installed"
fi
print_delimiter

# -----------------------------------------------------------------------------
# Install Firefox

if ! command -v firefox >/dev/null 2>&1; then
    print_info "[~] Install Firefox (for HTML reports and web screenshots)"
    apt-get install -y firefox-esr
    if command -v firefox >/dev/null 2>&1; then
        print_success "[+] Firefox installed successfully"
    else
        print_error "[!] An error occurred during Firefox install"
        exit 1
    fi   
else
    print_success "[+] Firefox is already installed"
fi
print_delimiter

# -----------------------------------------------------------------------------
# Install Geckodriver

if ! command -v geckodriver >/dev/null 2>&1; then
    print_info "[~] Install Geckodriver (for web screenshots)"
    apt-get install -y geckodriver
    if command -v geckodriver >/dev/null 2>&1; then
        print_success "[+] Geckodriver installed successfully"
    else
        print_error "[!] An error occurred during Geckodriver install"
        exit 1
    fi
else
    print_success "[+] Geckodriver is already installed"
fi
print_delimiter

# -----------------------------------------------------------------------------

print_info "[~] Install Python3 libraries required by Jok3r (if missing)"
"${VENV_PIP}" install -r "${SCRIPT_DIR}/requirements.txt"
if [ $? -ne 0 ]; then
    print_error "[!] Failed to install Jok3r Python requirements"
    exit 1
fi
"${VENV_PIP}" install --upgrade requests
if [ $? -ne 0 ]; then
    print_error "[!] Failed to upgrade requests inside the Jok3r virtual environment"
    exit 1
fi
print_delimiter

# -----------------------------------------------------------------------------

print_info "[~] Disable UserWarning related to psycopg2"
"${VENV_PIP}" uninstall psycopg2-binary -y
"${VENV_PIP}" uninstall psycopg2 -y
"${VENV_PIP}" install psycopg2-binary
print_delimiter

# -----------------------------------------------------------------------------

print_info "[~] Cleaning apt cache..."
apt-get clean
rm -rf /var/lib/apt/lists/*
print_delimiter

# -----------------------------------------------------------------------------

print_success "[~] Dependencies installation finished."
print_success "[~] IMPORTANT: Make sure to check if any error has been raised"
echo
