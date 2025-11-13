#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib.smartmodules.matchstrings.MatchStrings import creds_match


creds_match['snmp'] = {

    'metasploit': {
        'Login Successful: (?P<m1>\S+)': {
            'user': '',
            'pass': '$1',
        },
    },
    'snmpwn': {
        '\\[\\+\\]\\s*(?:Valid|Working) credentials:?\\s*(?P<m1>[^:\s]+):(?P<m2>[^\s]+)': {
            'user': '$1',
            'pass': '$2',
        },
    },

}
