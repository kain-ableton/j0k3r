#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lib.smartmodules.matchstrings.MatchStrings import products_match

WIG_REGEXP = '{}\s*[VERSION]\s*Platform'
WIG_REGEXP2 = '- Found platform {}(\s*[VERSION])?'


products_match['http']['web-language'] = {
    'Microsoft/ASP.NET': {
        'wappalyzer': 'Microsoft ASP.NET',
        'wig': [
            WIG_REGEXP.format('ASP\.NET'),
            WIG_REGEXP2.format('ASP\.NET'),
        ],
        'whatweb': '(?i)X-Powered-By\\[ASP\.NET(/[VERSION])?\\]',
    },
    'CFML': {
        'wappalyzer': 'CFML',
    },
    'Go': {
        'wappalyzer': 'Go',
    },
    'Java': {
        'wappalyzer': 'Java',
    },
    'Lua': {
        'wappalyzer': 'Lua',
    },
    'Node.js': {
        'wappalyzer': 'Node.js',
        'whatweb': '(?i)(PoweredBy|X-Powered-By)\\[Node\.js(/[VERSION])?\\]',
    },
    'Perl': {
        'wappalyzer': 'Perl',
    },
    'PHP': {
        'wappalyzer': 'PHP',
        'wig': [
            WIG_REGEXP.format('PHP'),
            WIG_REGEXP2.format('PHP'),
        ],
        'whatweb': '(?i)(PoweredBy|X-Powered-By)\\[PHP(/[VERSION])?\\]',
    },
    'Python': {
        'wappalyzer': 'Python',
        'whatweb': '(?i)(PoweredBy|X-Powered-By)\\[Python(/[VERSION])?\\]',
    },
    'Ruby': {
        'wappalyzer': 'Ruby',
        'whatweb': '(?i)(PoweredBy|X-Powered-By)\\[Ruby(/[VERSION])?\\]',
    },
}
