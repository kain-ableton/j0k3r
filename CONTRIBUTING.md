# Contributing to Jok3r

Thank you for your interest in contributing to Jok3r! This document provides guidelines and standards for contributing to the project.

## Table of Contents

- [Code Style Guidelines](#code-style-guidelines)
- [Python Import Organization](#python-import-organization)
- [Shell Script Standards](#shell-script-standards)
- [Logging Standards](#logging-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)

## Code Style Guidelines

### Python Code Style

Jok3r follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines with some project-specific conventions.

#### General Principles

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters (soft limit), 120 (hard limit)
- Use meaningful variable and function names
- Add docstrings to all public modules, functions, classes, and methods
- Keep functions focused and single-purpose

#### File Headers

All Python files should start with the standard header:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###
### Module > Description
###
```

## Python Import Organization

Imports must be organized according to PEP 8 standards in three distinct groups, separated by blank lines:

### Import Order

1. **Standard Library Imports** - Built-in Python modules
2. **Third-Party Imports** - External packages installed via pip
3. **Local/Application Imports** - Project-specific modules

### Example

```python
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
```

### Import Guidelines

- **Alphabetically sort** imports within each group
- **Use absolute imports** when possible (e.g., `from lib.core.Config import *`)
- **Avoid wildcard imports** (`from module import *`) except for:
  - `from lib.core.Config import *`
  - `from lib.core.Constants import *`
  - `from lib.utils.ArgParseUtils import *`
- **Group multiple imports** from the same module using parentheses:

```python
from lib.core.Exceptions import (
    ArgumentsException,
    AttackException,
    EnvironmentException,
)
```

### Common Import Patterns

**For controllers:**
```python
from lib.controller.BaseController import BaseController
```

**For database operations:**
```python
from lib.db.Session import session_scope
from lib.db.Mission import Mission
```

**For utilities:**
```python
from lib.utils.NetUtils import NetUtils
from lib.utils.FileUtils import FileUtils
```

**For output:**
```python
from lib.output.Logger import logger
from lib.output.Output import Output
```

### Tools

Use `isort` to automatically organize imports:
```bash
pip install isort
isort --profile black path/to/file.py
```

See `lib/utils/ImportHelper.py` for detailed import organization documentation.

## Shell Script Standards

All shell scripts in Jok3r follow consistent patterns for functions, error handling, and output.

### Script Header

All shell scripts should start with:

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```

This ensures:
- `set -e`: Exit on error
- `set -u`: Exit on undefined variable
- `set -o pipefail`: Catch errors in pipes
- `IFS`: Proper handling of whitespace

### Standard Output Functions

Use these standardized functions for all shell script output:

```bash
print_info() {
    BOLD_BLUE=$(tput bold ; tput setaf 4)
    NORMAL=$(tput sgr0)
    echo "${BOLD_BLUE}$1${NORMAL}"
}

print_success() {
    BOLD_GREEN=$(tput bold ; tput setaf 2)
    NORMAL=$(tput sgr0)
    echo "${BOLD_GREEN}$1${NORMAL}"
}

print_error() {
    BOLD_RED=$(tput bold ; tput setaf 1)
    NORMAL=$(tput sgr0)
    echo "${BOLD_RED}$1${NORMAL}" >&2
}

print_warning() {
    BOLD_YELLOW=$(tput bold ; tput setaf 3)
    NORMAL=$(tput sgr0)
    echo "${BOLD_YELLOW}$1${NORMAL}"
}
```

### Usage Examples

```bash
# Informational messages
print_info "[~] Starting installation..."

# Success messages
print_success "[+] Installation completed successfully"

# Error messages (sent to stderr, should typically exit)
print_error "[!] Installation failed"
exit 1

# Warning messages (non-fatal issues)
print_warning "[!] Some optional components were skipped"
```

### Error Handling

Always check command exit codes and handle errors:

```bash
# Check if command succeeded
if command -v git >/dev/null 2>&1; then
    print_success "[+] Git is installed"
else
    print_error "[!] Git is not installed"
    exit 1
fi

# Check script exit code
"${SCRIPT_DIR}/some-script.sh"
if [ $? -ne 0 ]; then
    print_error "[!] Script failed"
    exit 1
fi
```

### Exit Codes

Use consistent exit codes:
- `0`: Success
- `1`: General error
- Other specific codes as documented

## Logging Standards

Jok3r uses a centralized logging system with custom log levels and colored output.

### Available Log Levels

```python
from lib.output.Logger import logger

# Standard levels
logger.debug("Detailed debugging information")
logger.info("General informational messages")
logger.warning("Warning messages")
logger.error("Error messages")

# Custom levels
logger.success("Successful operation")
logger.prompt("User prompt/question")

# Smart module levels
logger.smartinfo("Smart module info")
logger.smartsuccess("Smart module success")
logger.smarterror("Smart module error")
```

### Log Level Guidelines

| Level | Symbol | Usage |
|-------|--------|-------|
| `debug()` | `[D]` | Detailed debugging information |
| `info()` | `[*]` | General informational messages |
| `success()` | `[+]` | Successful operations |
| `prompt()` | `[?]` | User prompts and questions |
| `warning()` | `[X]` | Warnings that don't stop execution |
| `error()` | `[!]` | Errors that may stop execution |
| `smartinfo()` | `[*] [SMART]` | Smart module informational messages |
| `smartsuccess()` | `[+] [SMART]` | Smart module success messages |
| `smarterror()` | `[!] [SMART]` | Smart module error messages |

### Logging Best Practices

1. **Use appropriate log levels**
   ```python
   logger.info("Starting service enumeration on port 80")
   logger.success("Found 5 potential vulnerabilities")
   logger.error("Failed to connect to target host")
   ```

2. **Keep messages concise and informative**
   - Start with action verbs when possible
   - Include relevant context (target, port, service, etc.)
   - Use consistent terminology

3. **Use string formatting for dynamic messages**
   ```python
   logger.info("Processing target: {}".format(target))
   logger.success("Completed scan in {:.2f} seconds".format(elapsed))
   ```

4. **Don't log sensitive information**
   - Avoid logging passwords, API keys, or tokens
   - Be cautious with user data and credentials
   - Use debug level for sensitive diagnostic info

5. **Handle exceptions appropriately**
   ```python
   try:
       risky_operation()
   except Exception as e:
       logger.error("Operation failed: {}".format(e))
       logger.debug("Stack trace:", exc_info=True)
   ```

### Configuration

Logging is configured centrally in `lib/core/LoggerConfig.py`. To change the log level:

```python
from lib.core.LoggerConfig import set_log_level

set_log_level('DEBUG')  # Show all messages including debug
set_log_level('INFO')   # Default level
```

See `lib/core/LoggerConfig.py` for detailed logging documentation and configuration options.

## Testing Guidelines

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test file
python3 -m pytest tests/test_session_scope.py

# Run with verbose output
python3 -m pytest tests/ -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names
- Include docstrings explaining what is being tested
- Follow existing test patterns in the repository

### Test Structure

```python
"""Test module for feature X."""
import pytest
from lib.module import feature


def test_feature_basic():
    """Test basic functionality of feature."""
    result = feature()
    assert result is not None


def test_feature_edge_case():
    """Test edge case handling in feature."""
    with pytest.raises(ValueError):
        feature(invalid_input)
```

## Pull Request Process

1. **Fork the repository** and create your branch from `master`
2. **Follow the code style guidelines** in this document
3. **Update documentation** if you're changing functionality
4. **Add tests** for new features when appropriate
5. **Ensure all tests pass** before submitting
6. **Write clear commit messages** that describe your changes
7. **Reference related issues** in your PR description

### Commit Message Format

```
Brief summary of changes (50 chars or less)

More detailed explanation if needed. Wrap at 72 characters.
Include motivation for the change and contrast with previous behavior.

- Bullet points are okay
- Use present tense: "Add feature" not "Added feature"
- Reference issues: "Fixes #123" or "Related to #456"
```

### Code Review

- Be open to feedback and discussion
- Address review comments promptly
- Update your PR based on feedback
- Maintain a respectful and collaborative tone

## Questions?

If you have questions about contributing, please:
- Open an issue for discussion
- Check existing issues and documentation
- Reach out to the maintainers

Thank you for contributing to Jok3r!
