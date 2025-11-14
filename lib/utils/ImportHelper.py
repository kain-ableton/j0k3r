#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###
### Utils > Import Helper
###
"""
Import organization helper and documentation for Jok3r.

This module provides guidelines and documentation for organizing imports
according to PEP 8 standards.

PEP 8 Import Guidelines:
========================

Imports should be organized in three groups, separated by blank lines:

1. Standard Library Imports
   - Built-in Python modules (os, sys, json, etc.)
   
2. Third-Party Imports  
   - External packages installed via pip (requests, sqlalchemy, etc.)
   
3. Local/Application Imports
   - Project-specific modules (lib.core.*, lib.utils.*, etc.)

Within each group:
- Imports should be alphabetically sorted
- Use absolute imports when possible
- Avoid wildcard imports (from module import *) except for specific cases

Example of Properly Organized Imports:
======================================

    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-
    ###
    ### Module > Description
    ###
    
    # Standard library imports
    import json
    import os
    import sys
    from collections import defaultdict
    from pathlib import Path
    
    # Third-party imports
    import requests
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Local imports
    from lib.core.Config import *
    from lib.core.Constants import *
    from lib.output.Logger import logger
    from lib.utils.FileUtils import FileUtils

Specific Jok3r Conventions:
===========================

1. Standard Library Imports:
   - Group by module type if there are many imports
   - Use absolute imports: import os, not from . import os
   
2. Third-Party Imports:
   - Common packages: requests, sqlalchemy, colorlog, etc.
   - Web-related: selenium, beautifulsoup4
   - Testing: pytest (only in test files)
   
3. Local Imports:
   - Always use absolute imports starting with 'lib.'
   - Config and Constants often imported with wildcard: from lib.core.Config import *
   - Logger should be imported last in the local section
   - Database models: from lib.db.Model import Model
   - Utils: from lib.utils.UtilName import UtilName
   - Output: from lib.output.Logger import logger

Import Order Exceptions:
=======================

1. Config wildcard imports are acceptable:
   from lib.core.Config import *
   from lib.core.Constants import *
   
2. ArgParseUtils may use wildcards for helper functions:
   from lib.utils.ArgParseUtils import *

3. When importing multiple items from same module, use parentheses:
   from lib.core.Exceptions import (
       ArgumentsException,
       AttackException,
       EnvironmentException
   )

Common Import Patterns:
======================

For controllers:
    from lib.controller.BaseController import BaseController
    
For database operations:
    from lib.db.Session import session_scope
    from lib.db.Mission import Mission
    
For utilities:
    from lib.utils.NetUtils import NetUtils
    from lib.utils.FileUtils import FileUtils
    
For output:
    from lib.output.Logger import logger
    from lib.output.Output import Output

Avoiding Common Issues:
======================

1. Circular imports: 
   - Use late imports (import inside function) if needed
   - Restructure code to remove circular dependencies
   
2. Import side effects:
   - Be aware that importing lib.output.Logger configures logging
   - Config modules may set global state
   
3. Performance:
   - Import expensive modules only when needed
   - Consider lazy imports for optional features

Tools for Import Organization:
=============================

Use isort for automatic import organization:
    pip install isort
    isort --profile black path/to/file.py
    
Use autopep8 for PEP 8 formatting:
    pip install autopep8
    autopep8 --in-place --aggressive path/to/file.py
"""


def validate_import_order(filepath):
    """
    Validate that imports in a Python file follow the standard order.
    
    This is a simple validation function that checks if imports are grouped
    correctly according to PEP 8 standards.
    
    Args:
        filepath (str): Path to the Python file to validate
        
    Returns:
        tuple: (is_valid, issues) where is_valid is a boolean and issues is a
               list of strings describing any problems found
    """
    import ast
    import os
    
    if not os.path.exists(filepath):
        return False, ["File does not exist"]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, [f"Could not read file: {e}"]
    
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return False, [f"Syntax error in file: {e}"]
    
    # Extract imports in order
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module_name = getattr(node, 'module', None)
            if module_name is None and isinstance(node, ast.Import):
                module_name = node.names[0].name
            imports.append(module_name or '')
    
    # Simple validation - just check that we have imports
    if not imports:
        return True, []  # No imports is valid
    
    issues = []
    
    # Check for common issues
    stdlib_after_local = False
    thirdparty_after_local = False
    
    local_seen = False
    for imp in imports:
        if imp.startswith('lib.'):
            local_seen = True
        elif local_seen:
            # After seeing local imports, check if we see stdlib or third-party
            if imp in ['os', 'sys', 'json', 're', 'collections', 'pathlib']:
                stdlib_after_local = True
            elif imp and not imp.startswith('lib.'):
                thirdparty_after_local = True
    
    if stdlib_after_local:
        issues.append("Standard library imports found after local imports")
    if thirdparty_after_local:
        issues.append("Third-party imports found after local imports")
    
    return len(issues) == 0, issues


# Standard library import examples for quick reference
STDLIB_IMPORTS = [
    'os', 'sys', 'json', 're', 'time', 'datetime', 'collections',
    'pathlib', 'subprocess', 'logging', 'argparse', 'configparser',
    'socket', 'threading', 'multiprocessing', 'traceback', 'copy'
]

# Common third-party imports in Jok3r
THIRDPARTY_IMPORTS = [
    'requests', 'sqlalchemy', 'colorlog', 'bs4', 'selenium',
    'git', 'cmd2', 'colored', 'prettytable', 'libnmap'
]

# Common local import patterns in Jok3r  
LOCAL_IMPORT_PATTERNS = [
    'from lib.core.Config import *',
    'from lib.core.Constants import *',
    'from lib.output.Logger import logger',
    'from lib.db.Session import session_scope',
    'from lib.utils.FileUtils import FileUtils',
    'from lib.utils.NetUtils import NetUtils',
]
