#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###
### Core > Logger Configuration
###
"""
Centralized logging configuration for Jok3r.

This module provides standardized logging setup with colorlog support,
custom log levels, and consistent formatting across the application.

Usage:
    from lib.core.LoggerConfig import get_logger
    
    logger = get_logger()
    logger.info("Informational message")
    logger.success("Success message")
    logger.error("Error message")
    logger.warning("Warning message")
    logger.debug("Debug message")
    logger.prompt("Prompt message")
    logger.smartinfo("Smart module info")
    logger.smartsuccess("Smart module success")
    logger.smarterror("Smart module error")

Log Levels:
    - DEBUG: Detailed debugging information
    - INFO: General informational messages
    - SUCCESS: Successful operation messages (custom level)
    - PROMPT: User prompt messages (custom level)
    - WARNING: Warning messages for potential issues
    - ERROR: Error messages for failures
    - SMARTINFO: Smart module informational messages (custom level)
    - SMARTSUCCESS: Smart module success messages (custom level)
    - SMARTERROR: Smart module error messages (custom level)

Configuration:
    The logger is configured with:
    - Colored output using colorlog
    - Custom log levels for SUCCESS, PROMPT, and SMART* messages
    - Consistent format: [LEVEL] message
    - Default log level: INFO
    - Suppressed urllib3 logging (set to CRITICAL)
"""
import logging

import colorlog

# Custom log level symbols
DEBUG = '[D]'
INFO = '[*]'
SUCCESS = '[+]'
PROMPT = '[?]'
WARNING = '[X]'
ERROR = '[!]'
SMARTINFO = '[*] [SMART]'
SMARTSUCCESS = '[+] [SMART]'
SMARTERROR = '[!] [SMART]'

# Colorlog format configuration
# https://github.com/borntyping/python-colorlog
LOG_FORMAT = '%(log_color)s%(levelname)s%(reset)s %(message_log_color)s%(message)s'
DATE_FORMAT = '%H:%M:%S'

# Color mapping for log levels
LOG_COLORS = {
    DEBUG: 'bold,white',
    INFO: 'bold,blue',
    SUCCESS: 'bold,green',
    PROMPT: 'bold,cyan',
    WARNING: 'bold,yellow',
    ERROR: 'bold,red',
    SMARTINFO: 'bold,blue',
    SMARTSUCCESS: 'bold,green',
    SMARTERROR: 'bold,red',
}

# Secondary color mapping for message text
SECONDARY_LOG_COLORS = {
    'message': {
        DEBUG: 'white',
        SUCCESS: 'green',
        WARNING: 'yellow',
        ERROR: 'red',
        SMARTSUCCESS: 'green',
        SMARTERROR: 'red',
    }
}

# Custom log level numeric values
# These must not conflict with standard logging levels:
# CRITICAL=50, ERROR=40, WARNING=30, INFO=20, DEBUG=10, NOTSET=0
LEVEL_SUCCESS = 35
LEVEL_PROMPT = 36
LEVEL_SMARTINFO = 37
LEVEL_SMARTSUCCESS = 38
LEVEL_SMARTERROR = 39


def configure_logger():
    """
    Configure and return the application logger with custom levels and formatting.
    
    This function sets up:
    - A colorlog handler with custom formatting
    - Custom log levels (SUCCESS, PROMPT, SMARTINFO, SMARTSUCCESS, SMARTERROR)
    - Custom methods on the logger instance
    - Default log level of INFO
    - Suppressed urllib3 logging
    
    Returns:
        logging.Logger: Configured logger instance with custom levels
    """
    logger = colorlog.getLogger()
    
    # Clear any existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()
    
    handler = colorlog.StreamHandler()
    
    formatter = colorlog.ColoredFormatter(
        LOG_FORMAT,
        datefmt=DATE_FORMAT,
        reset=True,
        log_colors=LOG_COLORS,
        secondary_log_colors=SECONDARY_LOG_COLORS,
        style='%'
    )
    handler.setFormatter(formatter)
    
    # Add custom levels to the logging module
    # https://gist.github.com/hit9/5635505
    logging.SUCCESS = LEVEL_SUCCESS
    logging.PROMPT = LEVEL_PROMPT
    logging.SMARTINFO = LEVEL_SMARTINFO
    logging.SMARTSUCCESS = LEVEL_SMARTSUCCESS
    logging.SMARTERROR = LEVEL_SMARTERROR
    
    # Register custom level names
    logging.addLevelName(logging.DEBUG, DEBUG)
    logging.addLevelName(logging.INFO, INFO)
    logging.addLevelName(logging.SUCCESS, SUCCESS)
    logging.addLevelName(logging.PROMPT, PROMPT)
    logging.addLevelName(logging.WARNING, WARNING)
    logging.addLevelName(logging.ERROR, ERROR)
    logging.addLevelName(logging.SMARTINFO, SMARTINFO)
    logging.addLevelName(logging.SMARTSUCCESS, SMARTSUCCESS)
    logging.addLevelName(logging.SMARTERROR, SMARTERROR)
    
    # Add custom methods to logger instance
    setattr(logger, 'success',
            lambda message, *args: logger._log(logging.SUCCESS, message, args))
    setattr(logger, 'prompt',
            lambda message, *args: logger._log(logging.PROMPT, message, args))
    setattr(logger, 'smartinfo',
            lambda message, *args: logger._log(logging.SMARTINFO, message, args))
    setattr(logger, 'smartsuccess',
            lambda message, *args: logger._log(logging.SMARTSUCCESS, message, args))
    setattr(logger, 'smarterror',
            lambda message, *args: logger._log(logging.SMARTERROR, message, args))
    
    # Set default log level
    logger.setLevel('INFO')
    logger.addHandler(handler)
    
    # Suppress verbose urllib3 logging
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    
    return logger


def get_logger():
    """
    Get the configured application logger instance.
    
    If the logger hasn't been configured yet, this returns the root logger.
    For a properly configured logger, use configure_logger() first or import
    the logger from lib.output.Logger.
    
    Returns:
        logging.Logger: The logger instance
    """
    logger = logging.getLogger()
    # Check if logger has been configured (has handlers)
    if not logger.handlers:
        # Return unconfigured logger - caller should configure it
        pass
    return logger


def set_log_level(level):
    """
    Set the logging level for the application logger.
    
    Args:
        level (str or int): Log level (e.g., 'DEBUG', 'INFO', logging.DEBUG)
    """
    logger = get_logger()
    logger.setLevel(level)


# Best Practices for Logging in Jok3r:
#
# 1. Use appropriate log levels:
#    - logger.debug() for detailed debugging information
#    - logger.info() for general informational messages
#    - logger.success() for successful operations
#    - logger.warning() for warnings that don't stop execution
#    - logger.error() for errors that may stop execution
#    - logger.prompt() for user prompts and questions
#    - logger.smartinfo/smartsuccess/smarterror() for smart module messages
#
# 2. Keep log messages concise and informative:
#    logger.info("Starting service enumeration on port 80")
#    logger.success("Found 5 potential vulnerabilities")
#    logger.error("Failed to connect to target host")
#
# 3. Use string formatting for dynamic messages:
#    logger.info("Processing target: {}".format(target))
#    logger.success("Completed scan in {:.2f} seconds".format(elapsed))
#
# 4. Don't log sensitive information:
#    - Avoid logging passwords, API keys, or tokens
#    - Be cautious with user data and credentials
#
# 5. Use consistent formatting within modules:
#    - Start messages with action verbs when possible
#    - Use consistent terminology across modules
#
# 6. Handle exceptions appropriately:
#    try:
#        risky_operation()
#    except Exception as e:
#        logger.error("Operation failed: {}".format(e))
#        logger.debug("Stack trace:", exc_info=True)
