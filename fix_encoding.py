#!/usr/bin/env python3
# fix_encoding.py - Fix UTF-8 BOM encoding

import os
import sys

files_to_fix = [
    'upstox_auth.py',
    'upstox_client.py',
    'nifty_scanner_app.py'
]

for filename in files_to_fix:
    if os.path.exists(filename):
        print(f"Fixing {filename}...")
        # Read with UTF-8 BOM
        with open(filename, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        # Write without BOM
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed {filename}")
    else:
        print(f"⚠️  {filename} not found")

print("\n✅ All files fixed! Try running again:")
print("python upstox_auth.py")
