from __future__ import annotations
from lib.smartmodules.matchstrings.MatchStrings import get_products_match
pm = get_products_match()

def buckets(svc: str, names: list[str]):
    svc_map = pm.setdefault(svc, {})
    for n in names:
        svc_map.setdefault(n, [])

# HTTP buckets commonly referenced by settings/*.conf
buckets("http", [
    "web-application-firewall", "web-appserver", "web-cms", "web-language",
    "web-framework", "web-jslib", "web-server", "https", "webdav", "htaccess"
])

# Databases / auth state buckets
for svc, server_key in [("mysql","mysql-server"),("postgresql","postgresql-server"),
                        ("mssql","mssql-server"),("oracle","oracle-server")]:
    buckets(svc, [server_key, "version_known", "auth_status"])

# SSH / FTP / TELNET / VNC / SNMP / SMB / AJP / RMI
buckets("ssh",    ["ssh-server", "version_known", "auth_status"])
buckets("ftp",    ["ftp-server", "version_known", "auth_status", "ftps"])
buckets("telnet", ["auth_status"])
buckets("vnc",    ["auth_status"])
buckets("snmp",   ["auth_status"])
buckets("smb",    ["os", "auth_status"])
buckets("ajp",    ["ajp-server", "version_known", "auth_status"])
buckets("rmi",    ["jmx"])

# Oracle specifics
buckets("oracle", ["sid"])

# Aliases already handled elsewhere (e.g., 'web-appserver' for ajp/oracle) remain intact.
