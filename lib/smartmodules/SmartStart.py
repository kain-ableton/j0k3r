#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###
# SmartModules > Smart Start
###
import ast
import pprint
import re

from lib.output.Logger import logger
from lib.output.Output import Output
from lib.smartmodules.ContextUpdater import ContextUpdater
from lib.smartmodules.MatchstringsProcessor import MatchstringsProcessor
from lib.smartmodules.matchstrings.registry import *


class SmartStart:

    def __init__(self, service):
        """
        SmartStart class allows to run code at the beginning of an attack
        against one service (before running any check). It is useful to initialize
        the target's context according to basic information already available (e.g 
        banner, url...) or that can be quickly retrieved from target (e.g. web 
        technologies).

        :param Service service: Target Service model
        """
        self.service = service
        self.cu = ContextUpdater(self.service)

    def _apply_findings(self, processor):
        """Apply findings from MatchstringsProcessor to ContextUpdater"""
        for option, patterns in processor.found_options.items():
            if patterns:
                self.cu.add_option(option, 'true')
        
        for product_type, patterns in processor.found_products.items():
            if patterns:
                self.cu.add_product(product_type, patterns[0], '')
        
        for os_name, patterns in processor.found_os.items():
            if patterns:
                self.cu.add_os(os_name)

    def run(self):
        """Initialize the context for the targeted service"""
        logger.smartinfo('SmartStart processing to initialize context...')

        # Detect if encrypted protocol (SSL/TLS) from original service name
        # (from Nmap/Shodan)
        processor = MatchstringsProcessor(self.service, [self.service.name_original])
        processor.detect_specific_options()
        self._apply_findings(processor)
        self.cu.update()

        # Update context from banner
        processor = MatchstringsProcessor(self.service, [self.service.banner])
        processor.detect_products()
        processor.detect_specific_options()
        if not self.service.host.os:
            processor.detect_os()
        self._apply_findings(processor)
        self.cu.update()

        # Run start method corresponding to target service if available
        list_methods = [method_name for method_name in dir(self)
                        if callable(getattr(self, method_name))]
        start_method_name = 'start_{}'.format(self.service.name)
        if start_method_name in list_methods:
            start_method = getattr(self, start_method_name)
            start_method()
            self.cu.update()

    # ------------------------------------------------------------------------------------

    def start_http(self):
        """Method run specifically for HTTP services"""

        # Autodetect HTTPS
        if self.service.url.lower().startswith('https://'):
            logger.smartinfo('HTTPS protocol detected from URL')
            self.cu.add_option('https', 'true')

        # Check if HTTP service is protected by .htaccess authentication
        if self.service.http_headers \
                and '401 Unauthorized'.lower() in self.service.http_headers.lower():

            logger.smartinfo('HTTP authentication (htaccess) detected '
                             '(401 Unauthorized)')
            self.cu.add_option('htaccess', 'true')

        # Update context with web technologies
        if self.service.web_technos:
            # Detect OS
            if not self.service.host.os:
                processor = MatchstringsProcessor(self.service, [self.service.host.os])
                processor.detect_os()
                self._apply_findings(processor)

            # Detect products
            try:
                technos = ast.literal_eval(self.service.web_technos)
            except Exception as e:
                logger.debug('Error when retrieving "web_technos" field '
                             'from db: {}'.format(e))
                technos = []

            for t in technos:
                for prodtype in products_match['http']:
                    p = products_match['http'][prodtype]
                    for prodname in p:
                        if 'wappalyzer' in p[prodname]:
                            pattern = p[prodname]['wappalyzer']

                            #m = re.search(pattern, t['name'], re.IGNORECASE|re.DOTALL)
                            if pattern.lower() == t['name'].lower():
                                version = t['version']
                                self.cu.add_product(
                                    prodtype, prodname, version)

                                # Move to next product type if something found
                                break
