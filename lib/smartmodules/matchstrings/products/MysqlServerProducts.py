#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib.smartmodules.matchstrings.registry import products_match

products_match['mysql']['mysql-server'] = {
    'MySQL': {
        'banner': 'MySQL(\s+[VERSION])?',
    },
}
