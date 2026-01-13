#!/usr/bin/env python3
"""
Fix all problematic Python files in your project using Claude AI
Runs auto_fix_with_claude.py on multiple files
"""

import subprocess
import sys

files_to_fix = [
    'upstox_auth.py',
    'upstox_client.py',
    'nifty_scanner_app.py'
]

def fix_all_files():
    """Fix all files using Claude API"""
    print("\n" + "="*50)
    print("Auto-fixing all files with Claude")
    print("="*50 + "\n")
    
    failed_files = []
    fixed_files = []
    
    for file in files_to_fix:
        print(f"\n{'='*50}")
        print(f"Fixing: {file}")
        print(f"{'='*50}")
        
        result = subprocess.run(
            ['python', 'auto_fix_with_claude.py', file, '5'],
            capture_output=False
        )
        
        if result.returncode == 0:
            fixed_files.append(file)
            print(f"SUCCESS: {file}")
        else:
            failed_files.append(file)
            print(f"FAILED: {file}")
    
    # Summary
    print(f"\n{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")
    print(f"Fixed: {len(fixed_files)}/{len(files_to_fix)}")
    
    if fixed_files:
        print(f"\nSuccessfully fixed:")
        for f in fixed_files:
            print(f"  [OK] {f}")
    
    if failed_files:
        print(f"\nFailed to fix:")
        for f in failed_files:
            print(f"  [FAIL] {f}")
        return 1
    
    print(f"\n✓ All files fixed successfully!")
    print(f"\nNext steps:")
    print(f"1. Test your code: python upstox_auth.py")
    print(f"2. Commit changes: git add . && git commit -m 'Fix: Auto-corrected code with Claude'")
    print(f"3. Push to GitHub: git push origin main")
    
    return 0

if __name__ == "__main__":
    sys.exit(fix_all_files())
