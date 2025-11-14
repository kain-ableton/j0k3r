#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###
# SmartModules > Smart Postcheck
###
from lib.output.Logger import logger
from lib.smartmodules.ContextUpdater import ContextUpdater
from lib.smartmodules.MatchstringsProcessor import MatchstringsProcessor


class SmartPostcheck:

    def __init__(self,
                 service,
                 tool_name,
                 cmd_output):
        """
        SmartPostcheck class allows to run code after a check during an attack 
        against one service. It is useful to analyze/process command outputs
        and to update context accordingly.

        :param Service service: Target service db model
        :param str tool_name: Name of the check that has been run before
        :param str cmd_output: Command output (sanitized / special chars removed)
            Important: output is prepended by command line
        """
        self.service = service
        self.tool_name = tool_name
        self.cmd_output = cmd_output
        self.cu = ContextUpdater(self.service)
        self.processor = MatchstringsProcessor(self.service, [self.cmd_output])

    def run(self):
        """Run postcheck processing"""

        logger.smartinfo('SmartPostcheck processing to update context...')
        self.processor.detect_credentials()
        self.processor.detect_specific_options()
        self.processor.detect_products()
        self.processor.detect_vulns()
        self._apply_findings()
        self.cu.update()

    def _apply_findings(self):
        """Apply findings from MatchstringsProcessor to ContextUpdater"""
        # Apply credentials
        for cred in self.processor.found_creds:
            username = cred.get('username', '')
            password = cred.get('password', '')
            cred_type = cred.get('type', 'credentials')
            if username or password:
                self.cu.add_credentials(username, password, cred_type)
        
        # Apply options
        for option, patterns in self.processor.found_options.items():
            if patterns:
                self.cu.add_option(option, 'true')
        
        # Apply products
        for product_type, patterns in self.processor.found_products.items():
            if patterns:
                self.cu.add_product(product_type, patterns[0], '')
        
        # Apply vulnerabilities
        for vuln_name, patterns in self.processor.found_vulns.items():
            if patterns:
                self.cu.add_vuln(vuln_name)
