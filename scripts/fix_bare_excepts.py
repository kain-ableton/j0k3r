#!/usr/bin/env python3
"""
Fix bare except clauses in the codebase.
This script identifies and helps fix bare 'except:' statements.
"""

import os
import re
from pathlib import Path

def find_bare_excepts(file_path):
    """Find bare except clauses in a Python file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    issues = []
    for i, line in enumerate(lines, 1):
        # Match bare except (not except SomeException or except ... as)
        if re.search(r'^\s*except\s*:\s*(?:#.*)?$', line):
            # Get context
            start = max(0, i-3)
            end = min(len(lines), i+3)
            context = ''.join(lines[start:end])
            issues.append({
                'line': i,
                'text': line.strip(),
                'context': context
            })
    
    return issues

def analyze_codebase(root_dir='lib'):
    """Analyze entire codebase for bare except clauses."""
    print("=" * 70)
    print("Bare Except Clause Analysis")
    print("=" * 70)
    print()
    
    total_files = 0
    total_issues = 0
    files_with_issues = []
    
    for root, dirs, files in os.walk(root_dir):
        # Skip virtualenvs
        dirs[:] = [d for d in dirs if 'virtualenv' not in d and d != '__pycache__']
        
        for file in files:
            if not file.endswith('.py'):
                continue
            
            total_files += 1
            file_path = os.path.join(root, file)
            issues = find_bare_excepts(file_path)
            
            if issues:
                files_with_issues.append((file_path, issues))
                total_issues += len(issues)
    
    # Report results
    print(f"Files scanned: {total_files}")
    print(f"Files with bare except: {len(files_with_issues)}")
    print(f"Total bare except clauses: {total_issues}")
    print()
    
    if files_with_issues:
        print("=" * 70)
        print("Details")
        print("=" * 70)
        print()
        
        for file_path, issues in files_with_issues:
            print(f"📁 {file_path}")
            for issue in issues:
                print(f"   Line {issue['line']}: {issue['text']}")
            print()
    
    # Generate fix suggestions
    if total_issues > 0:
        print("=" * 70)
        print("Suggested Fixes")
        print("=" * 70)
        print()
        print("1. Catch specific exceptions when possible:")
        print("   except ValueError as e:")
        print("   except (KeyError, AttributeError) as e:")
        print()
        print("2. If catching all exceptions, use Exception explicitly:")
        print("   except Exception as e:")
        print("       logger.exception('Error occurred: %s', e)")
        print()
        print("3. For cleanup code, use try-finally instead:")
        print("   try:")
        print("       do_something()")
        print("   finally:")
        print("       cleanup()")
        print()
        print("4. Document why broad exception is needed:")
        print("   except Exception as e:  # Catch all: plugin system must not crash")
        print()
        
        # Create backup recommendation
        print("Before fixing, create a backup branch:")
        print("  git checkout -b fix-bare-excepts")
        print()
    else:
        print("✓ No bare except clauses found!")
    
    return files_with_issues

if __name__ == '__main__':
    import sys
    
    root_dir = sys.argv[1] if len(sys.argv) > 1 else 'lib'
    
    print(f"Analyzing directory: {root_dir}")
    print()
    
    results = analyze_codebase(root_dir)
    
    if results:
        print("\n⚠️  Found bare except clauses that should be fixed.")
        print("See IMPROVEMENTS.md for detailed recommendations.")
        sys.exit(1)
    else:
        print("\n✓ Code quality check passed!")
        sys.exit(0)
