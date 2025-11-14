#!/usr/bin/env bash
# Quick implementation of suggested improvements
# Run this to implement easy fixes

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

echo "=================================================="
echo "Jok3r Quick Improvements Implementation"
echo "=================================================="
echo ""

# 1. Add development dependencies
echo "[1/5] Adding development dependencies..."
cat >> requirements-dev.txt << 'EOF'
# Development dependencies
pylint>=2.12.0
pytest>=7.0.0
pytest-cov>=3.0.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.950
pre-commit>=2.17.0
EOF

echo "✓ Created requirements-dev.txt"

# 2. Create pre-commit config
echo "[2/5] Creating pre-commit hooks..."
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 22.10.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 5.0.4
    hooks:
      - id: flake8
        args: ['--max-line-length=100', '--ignore=E203,W503']

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.3.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements
EOF

echo "✓ Created .pre-commit-config.yaml"

# 3. Create pytest config
echo "[3/5] Creating pytest configuration..."
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
EOF

echo "✓ Created pytest.ini"

# 4. Create pylint config
echo "[4/5] Creating pylint configuration..."
cat > .pylintrc << 'EOF'
[MASTER]
ignore=CVS,.git,__pycache__,toolbox,virtualenvs

[MESSAGES CONTROL]
disable=
    C0111,  # missing-docstring
    C0103,  # invalid-name
    R0913,  # too-many-arguments
    R0914,  # too-many-locals

[FORMAT]
max-line-length=100
indent-string='    '

[DESIGN]
max-args=8
max-attributes=12
EOF

echo "✓ Created .pylintrc"

# 5. Update .gitignore
echo "[5/5] Updating .gitignore..."
cat >> .gitignore << 'EOF'

# Development
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Logs
*.log
/tmp/

# Backups
*.bak
*.backup
*.old
EOF

echo "✓ Updated .gitignore"

echo ""
echo "=================================================="
echo "✓ Quick improvements implemented!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Install dev dependencies: pip install -r requirements-dev.txt"
echo "  2. Install pre-commit hooks: pre-commit install"
echo "  3. Run tests: pytest"
echo "  4. Run linter: pylint lib/"
echo "  5. Format code: black lib/"
echo ""
echo "See IMPROVEMENTS.md for more enhancement ideas."
