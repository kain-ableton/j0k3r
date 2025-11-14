# Jok3r Tool Management Guide

## Quick Commands

### Update Tools
```bash
# Update all installed tools
./quick-update.sh

# Update specific service tools
python3 jok3r.py toolbox --update http --auto

# Update specific tool
python3 jok3r.py toolbox --update-tool nmap --auto
```

### Install Tools
```bash
# Install all tools (WARNING: Takes hours and requires lots of disk space)
python3 jok3r.py toolbox --install-all --auto

# Install tools for specific service
./install-service-tools.sh http

# Install specific tool
python3 jok3r.py toolbox --install-tool nikto --auto
```

### View Toolbox Status
```bash
# Show all tools
python3 jok3r.py toolbox --show-all

# Show tools for specific service
python3 jok3r.py toolbox --show http

# Show only installed tools
python3 jok3r.py toolbox --show-all | grep "OK |"

# Show only missing tools
python3 jok3r.py toolbox --show-all | grep "Not installed"
```

### Check Tool Installation
```bash
# Check all installed tools
python3 jok3r.py toolbox --check
```

### Uninstall Tools
```bash
# Uninstall specific tool
python3 jok3r.py toolbox --uninstall-tool <tool-name>

# Uninstall all tools for a service
python3 jok3r.py toolbox --uninstall <service>

# Uninstall all tools
python3 jok3r.py toolbox --uninstall-all
```

## Tool Categories by Service

- **ajp**: AJP protocol testing
- **ftp**: FTP service testing
- **http**: Web application testing (largest category)
- **java-rmi**: Java RMI testing
- **jdwp**: Java Debug Wire Protocol
- **mssql**: Microsoft SQL Server
- **mysql**: MySQL/MariaDB
- **oracle**: Oracle Database
- **postgresql**: PostgreSQL
- **rdp**: Remote Desktop Protocol
- **smb**: SMB/CIFS
- **smtp**: Email/SMTP
- **snmp**: SNMP
- **ssh**: SSH
- **telnet**: Telnet
- **vnc**: VNC
- **multi**: Multi-service/General tools

## Installation Notes

### System Requirements
- Sufficient disk space (20-50GB for all tools)
- Internet connection
- Root/sudo access (for some tools)
- Python 3.10+

### Common Issues

**Tools fail to install:**
- Check system dependencies: `./install-dependencies.sh`
- Some tools require specific OS versions
- Some tools may be deprecated or have broken repositories

**Check command fails:**
- Tool may be installed but PATH not set correctly
- Try running manually from toolbox/<service>/<tool> directory

**Permission errors:**
- Some tools need to be run as root
- Virtual environments may need proper permissions

## Recommended Installation Strategy

1. **Start with core tools:**
```bash
./install-service-tools.sh multi
./install-service-tools.sh http
```

2. **Add services as needed:**
```bash
./install-service-tools.sh ssh
./install-service-tools.sh smb
```

3. **Keep tools updated:**
```bash
./quick-update.sh
```

## Tool Statistics (Current)

Run to see current stats:
```bash
python3 jok3r.py info --services
```

## More Information

- Full documentation: `./doc/`
- Tool configurations: `./settings/toolbox.conf`
- Service checks: `./settings/<service>.conf`
