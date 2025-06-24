#!/usr/bin/env python3
"""
Script to remove all mock data references from the codebase
"""
import os
import re

def clean_file(filepath):
    """Remove mock data references from a file"""
    print(f"Cleaning {filepath}...")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Remove mock_data import
    content = re.sub(r'from tools\.mock_data import mock_data\n', '', content)
    
    # Remove mock_data usage patterns
    content = re.sub(r'import os\n.*?from tools\.mock_data import mock_data\n', 'import os\n', content, flags=re.DOTALL)
    
    # Remove mock mode checks and their blocks
    # Pattern: use_mock = ... followed by if use_mock: ... (finding the matching else or try)
    
    # Find and remove mock mode blocks
    lines = content.split('\n')
    new_lines = []
    skip_until_else_or_try = False
    indent_level = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for mock mode check
        if 'use_mock = os.getenv("HABU_USE_MOCK_DATA"' in line:
            # Skip this line
            i += 1
            continue
            
        # Check for if use_mock:
        if skip_until_else_or_try:
            # Skip lines until we find try: or else: or function definition at same level
            if (line.strip().startswith('try:') or 
                line.strip().startswith('else:') or
                (line.strip() and not line.startswith(' ') and not line.startswith('\t'))):
                skip_until_else_or_try = False
                # Don't skip the try: line
                if not line.strip().startswith('else:'):
                    new_lines.append(line)
            i += 1
            continue
            
        if 'if use_mock:' in line:
            skip_until_else_or_try = True
            indent_level = len(line) - len(line.lstrip())
            i += 1
            continue
            
        new_lines.append(line)
        i += 1
    
    content = '\n'.join(new_lines)
    
    # Clean up any remaining mock references
    content = re.sub(r'.*mock_data\..*\n', '', content)
    content = re.sub(r'.*\(MOCK MODE\).*', '', content)
    content = re.sub(r'"mock_mode": true,?\n', '', content)
    content = re.sub(r'"mock_mode": True,?\n', '', content)
    
    # Remove empty lines that might have been created
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Remove empty try blocks
    content = re.sub(r'try:\s*\n\s*try:', 'try:', content)
    
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  ✅ Cleaned {filepath}")
        return True
    else:
        print(f"  ℹ️  No changes needed for {filepath}")
        return False

def main():
    """Clean all files with mock data references"""
    print("🧹 CLEANING MOCK DATA FROM CODEBASE")
    print("=" * 50)
    
    tools_dir = "tools"
    files_to_clean = [
        "tools/habu_list_partners.py",
        "tools/habu_list_templates.py", 
        "tools/habu_submit_query.py",
        "tools/habu_check_status.py",
        "tools/habu_get_results.py",
        "tools/habu_list_exports.py",
        "demo_api.py"
    ]
    
    cleaned_count = 0
    for filepath in files_to_clean:
        if os.path.exists(filepath):
            if clean_file(filepath):
                cleaned_count += 1
        else:
            print(f"  ⚠️  File not found: {filepath}")
    
    print(f"\n🎯 CLEANUP COMPLETE: {cleaned_count} files cleaned")
    
    # Also remove any environment variable references
    print("\n🔍 Checking for remaining mock references...")
    os.system("grep -r 'HABU_USE_MOCK_DATA' . --include='*.py' || echo 'No remaining mock references found'")

if __name__ == "__main__":
    main()