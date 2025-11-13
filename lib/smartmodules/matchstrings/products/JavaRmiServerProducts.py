#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib.smartmodules.matchstrings.registry import products_match

# TODO

products_match['java-rmi']['java-rmi-server'] = {
    'Oracle/Weblogic Server': {
        'barmie': '(?i)weblogic',
    },
    'JBoss': {
        'barmie': '(?i)jboss',
    },
    'Apache/Tomcat': {
        'barmie': '(?i)tomcat',
    },
}
