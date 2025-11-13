#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib.smartmodules.matchstrings.registry import products_match


products_match['ssh']['ssh-server'] = {
    'Openssh': {
        'banner': 'OpenSSH(\s+[VERSION])?',
    },
    'Dropbear SSH': {
        'banner': 'Dropbear sshd(\s+[VERSION])?',
    }
}
