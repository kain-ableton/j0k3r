#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib.smartmodules.matchstrings.registry import products_match

# List of most common web servers: https://en.wikipedia.org/wiki/Comparison_of_web_server_software

# Examples:
# product: Microsoft IIS httpd version: 6.0 ostype: Windows
# product: Apache httpd version: 2.2.4 extrainfo: (Unix) DAV/2
# product: Apache httpd version: 2.0.63 extrainfo: DAV/2 hostname

WIG_REGEXP = '{}\s*[VERSION]\s*Platform'
WIG_REGEXP2 = '- Found platform {}(\s*[VERSION])?'

products_match['http']['web-server'] = {

    'Apache': {
        'wappalyzer': 'Apache',
        'banner': 'Apache httpd(\s*[VERSION])?',
        'wig': [
            WIG_REGEXP.format('Apache'),
            WIG_REGEXP2.format('Apache'),
        ],
        'whatweb': '(?i)HTTPServer\\[Apache(/[VERSION])?\\]',
    },
    'Hiawatha': {
        'wappalyzer': 'Hiawatha',
        'banner': 'Hiawatha(\s*httpd)?(\s*[VERSION])?',
    },
    'IBM/HTTP Server': {
        'wappalyzer': 'IBM HTTP Server',
        'banner': 'IBM(\s*(HTTP Server|httpd))?(\s*[VERSION])?',
    },
    'Lighttpd': {
        'wappalyzer': 'lighttpd',
        'banner': 'lighttpd(\s*[VERSION])?',
        'whatweb': '(?i)HTTPServer\\[lighttpd(/[VERSION])?\\]',
    },
    'LiteSpeed Web Server': {
        'wappalyzer': 'LiteSpeed',
        'banner': 'LiteSpeed httpd(\s+[VERSION])?',
        'whatweb': '(?i)HTTPServer\\[LiteSpeed(/[VERSION])?\\]',
    },
    'Microsoft/IIS': {
        'wappalyzer': 'IIS',
        'banner': 'Microsoft IIS (httpd|WebDAV)(\s*[VERSION])?',
        'wig': [
            WIG_REGEXP.format('IIS'),
            WIG_REGEXP2.format('IIS'),
        ],
        'whatweb': '(?i)HTTPServer\\[Microsoft-IIS(/[VERSION])?\\]',
    },
    'Mongoose': {
        'banner': 'Mongoose httpd(\s*[VERSION])?',
    },
    'Monkey Http Daemon': {
        'wappalyzer': 'Monkey HTTP Server',
        'banner': 'Monkey httpd(\s*[VERSION])?',
    },
    'Nginx': {
        'wappalyzer': 'Nginx',
        'banner': 'nginx(\s*[VERSION])?',
        'wig': [
            WIG_REGEXP.format('nginx'),
            WIG_REGEXP2.format('nginx'),
        ],
        'whatweb': '(?i)HTTPServer\\[nginx(/[VERSION])?\\]',
    },
    'Oracle/Http Server': {
        'wappalyzer': 'Oracle HTTP Server',
        'banner': 'Oracle HTTP Server(\s*(9iAS httpd|Powered by Apache))?(.+\(version [VERSION]\))?',
        'whatweb': '(?i)HTTPServer\\[Oracle\s*HTTP\s*Server(/[VERSION])?\\]',
    },
    'Rejetto/Http File Server': {
        'banner': 'HttpFileServer httpd(\s*[VERSION])?',
    },
    'Thttpd': {
        'wappalyzer': 'thttpd',
        'banner': 'thttpd(\s*[VERSION])?',
    },
    'Yaws': {
        'wappalyzer': 'Yaws',
        'banner': 'Yaws httpd(\s*[VERSION])?',
    },
    'Zeus Web Server': {
        'banner': 'Zeus httpd(\s*Admin Server)?(\s*[VERSION])?',
    },
}
