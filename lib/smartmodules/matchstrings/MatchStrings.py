#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.smartmodules.matchstrings.registry import (
    VERSION_REGEXP,
    creds_match,
    options_match,
    os_match,
    products_match,
    vulns_match,
)


# ----------------------------------------------------------------------------------------
# Credentials
#
# Sample:
# creds_match['http'] = {
#     'tool-name': {
#         'found creds: (?P<m1>\S*):(?P<m2>\S*)': {
#             'user': '$1',
#             'pass': '$2',
#             'type': 'wordpress'
#         },
#         'found user: (?P<m1>\S*)': {
#             'user': '$1'
#         }
#     }
# }

from lib.smartmodules.matchstrings.os.OS import *
from lib.smartmodules.matchstrings.vulns.SshVulns import *
from lib.smartmodules.matchstrings.vulns.SmtpVulns import *
from lib.smartmodules.matchstrings.vulns.SmbVulns import *
from lib.smartmodules.matchstrings.vulns.RdpVulns import *
from lib.smartmodules.matchstrings.vulns.PostgresqlVulns import *
from lib.smartmodules.matchstrings.vulns.OracleVulns import *
from lib.smartmodules.matchstrings.vulns.MysqlVulns import *
from lib.smartmodules.matchstrings.vulns.MssqlVulns import *
from lib.smartmodules.matchstrings.vulns.JdwpVulns import *
from lib.smartmodules.matchstrings.vulns.JavaRmiVulns import *
from lib.smartmodules.matchstrings.vulns.HttpVulns import *
from lib.smartmodules.matchstrings.vulns.FtpVulns import *
from lib.smartmodules.matchstrings.products.SshServerProducts import *
from lib.smartmodules.matchstrings.products.SmtpServerProducts import *
from lib.smartmodules.matchstrings.products.PostgresqlServerProducts import *
from lib.smartmodules.matchstrings.products.OracleServerProducts import *
from lib.smartmodules.matchstrings.products.MysqlServerProducts import *
from lib.smartmodules.matchstrings.products.MssqlServerProducts import *
from lib.smartmodules.matchstrings.products.JavaRmiServerProducts import *
from lib.smartmodules.matchstrings.products.HttpWebServerProducts import *
from lib.smartmodules.matchstrings.products.HttpWebLanguageProducts import *
from lib.smartmodules.matchstrings.products.HttpWebJslibProducts import *
from lib.smartmodules.matchstrings.products.HttpWebFrameworkProducts import *
from lib.smartmodules.matchstrings.products.HttpWebCmsProducts import *
from lib.smartmodules.matchstrings.products.HttpWebApplicationFirewallProducts import *
from lib.smartmodules.matchstrings.products.HttpWebAppserverProducts import *
from lib.smartmodules.matchstrings.products.FtpServerProducts import *
from lib.smartmodules.matchstrings.products.AjpServerProducts import *
from lib.smartmodules.matchstrings.options.TelnetOptions import *
from lib.smartmodules.matchstrings.options.SmtpOptions import *
from lib.smartmodules.matchstrings.options.SmbOptions import *
from lib.smartmodules.matchstrings.options.OracleOptions import *
from lib.smartmodules.matchstrings.options.JavaRmiOptions import *
from lib.smartmodules.matchstrings.options.HttpOptions import *
from lib.smartmodules.matchstrings.options.FtpOptions import *
from lib.smartmodules.matchstrings.creds.VncCreds import *
from lib.smartmodules.matchstrings.creds.TelnetCreds import *
from lib.smartmodules.matchstrings.creds.SshCreds import *
from lib.smartmodules.matchstrings.creds.SnmpCreds import *
from lib.smartmodules.matchstrings.creds.SmtpCreds import *
from lib.smartmodules.matchstrings.creds.PostgresqlCreds import *
from lib.smartmodules.matchstrings.creds.OracleCreds import *
from lib.smartmodules.matchstrings.creds.MysqlCreds import *
from lib.smartmodules.matchstrings.creds.MssqlCreds import *
from lib.smartmodules.matchstrings.creds.JavaRmiCreds import *
from lib.smartmodules.matchstrings.creds.HttpCreds import *
from lib.smartmodules.matchstrings.creds.FtpCreds import *
from lib.smartmodules.matchstrings.creds.AjpCreds import *
