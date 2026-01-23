# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# fix_encoding.py - Fix UTF-8 BOM encoding with robust error handling

import os
import sys

files_to_fix = [
    'upstox_auth.py',
    'upstox_client.py',
    'nifty_scanner_app.py'
]

def try_read_file(filename):
    """Try reading file with multiple encodings"""
    encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, LookupError):
            continue
    
    # If all else fails, read as binary and decode with errors='replace'
    with open(filename, 'rb') as f:
        return f.read().decode('utf-8', errors='replace')

for filename in files_to_fix:
    if os.path.exists(filename):
        try:
            print(f"Fixing {filename}...")
            
            # Read with robust error handling
            content = try_read_file(filename)
            
            # Write without BOM
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Fixed {filename}")
        except Exception as e:
            print(f"✗ {filename} not found or error: {e}")
    else:
        print(f"✗ {filename} not found")

print("\n✓ All files fixed! Try running again:")
print("python upstox_auth.py")
