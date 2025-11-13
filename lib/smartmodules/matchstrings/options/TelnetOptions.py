#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib.smartmodules.matchstrings.registry import options_match


options_match['telnet'] = {

    'grabtelnet': {
        'TLS/SSL enabled telnet client MUST be used to connect': {
            'name': 'telnets',
            'value': 'true',
        },
    },

}
