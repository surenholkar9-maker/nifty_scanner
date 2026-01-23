# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# fix_encoding_final.py - Fix all encoding issues including UTF-16

import os
import sys
import chardet

files_to_fix = [
    'upstox_auth.py',
    'upstox_client.py',
    'nifty_scanner_app.py'
]

def detect_and_fix_encoding(filename):
    """Detect actual encoding and convert to UTF-8"""
    try:
        # Read as binary to detect encoding
        with open(filename, 'rb') as f:
            raw_data = f.read()
        
        # Try chardet detection
        detected = chardet.detect(raw_data)
        detected_encoding = detected.get('encoding', 'utf-8')
        
        print(f"  Detected encoding: {detected_encoding}")
        
        # Try to decode with detected encoding
        try:
            content = raw_data.decode(detected_encoding)
        except (UnicodeDecodeError, LookupError):
            # Fallback encodings
            for encoding in ['utf-16', 'utf-16-le', 'utf-16-be', 'latin-1', 'cp1252']:
                try:
                    content = raw_data.decode(encoding)
                    print(f"  Fallback to: {encoding}")
                    break
                except (UnicodeDecodeError, LookupError):
                    continue
            else:
                # Last resort
                content = raw_data.decode('utf-8', errors='replace')
                print(f"  Using UTF-8 with error replacement")
        
        # Remove BOM if present
        if content.startswith('\ufeff'):
            content = content[1:]
        
        # Write as clean UTF-8
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False

print("🔧 Fixing encoding issues...\n")

for filename in files_to_fix:
    if os.path.exists(filename):
        print(f"Fixing {filename}...")
        if detect_and_fix_encoding(filename):
            print(f"✓ {filename} fixed!\n")
        else:
            print(f"✗ {filename} failed\n")
    else:
        print(f"✗ {filename} not found\n")

print("✓ All files fixed!")
