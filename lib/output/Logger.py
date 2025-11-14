#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###
### Output > Logger
###
"""
Logger module for Jok3r.

This module provides the logger instance configured via LoggerConfig.
Import the logger from this module throughout the application.

Usage:
    from lib.output.Logger import logger
    
    logger.info("Information message")
    logger.success("Success message")
    logger.error("Error message")
    
See lib.core.LoggerConfig for detailed documentation on:
- Available log levels and methods
- Configuration options
- Best practices for logging
"""
# Import configuration from centralized LoggerConfig
from lib.core.LoggerConfig import (
    configure_logger,
    DEBUG,
    INFO,
    SUCCESS,
    PROMPT,
    WARNING,
    ERROR,
    SMARTINFO,
    SMARTSUCCESS,
    SMARTERROR,
)

# Configure and export the logger instance
logger = configure_logger()

# Export log level constants for convenience
__all__ = [
    'logger',
    'DEBUG',
    'INFO',
    'SUCCESS',
    'PROMPT',
    'WARNING',
    'ERROR',
    'SMARTINFO',
    'SMARTSUCCESS',
    'SMARTERROR',
]

