# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Auto-fix Python code errors using Claude AI
Runs any Python script and automatically fixes errors using Claude API
"""

import subprocess
import sys
import os
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = Anthropic()

def read_file(filepath):
    """Read file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with error replacement
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()

def write_file(filepath, content):
    """Write file content"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def get_claude_fix(error_msg, file_path, code_content):
    """Get fix from Claude for the error"""
    prompt = f"""You are an expert Python developer. Fix this Python error:

File: {file_path}
Error: {error_msg}

Current Code:
```python
{code_content}
```

IMPORTANT RULES:
1. Return ONLY the corrected Python code
2. Keep all original functionality
3. Add no explanations or markdown
4. Make minimal changes necessary to fix the error
5. If it's an encoding issue, ensure UTF-8 encoding
6. Fix all related issues to prevent cascading errors

Return ONLY the corrected code:"""

    print("🤖 Asking Claude for fix...")
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    fixed_code = response.content[0].text
    
    # Clean up if Claude wrapped it in markdown
    if fixed_code.startswith('```python'):
        fixed_code = fixed_code[9:]
    if fixed_code.startswith('```'):
        fixed_code = fixed_code[3:]
    if fixed_code.endswith('```'):
        fixed_code = fixed_code[:-3]
    
    fixed_code = fixed_code.strip()
    return fixed_code

def run_python_file(filepath):
    """Run a Python file and return result"""
    try:
        result = subprocess.run(
            ['python', filepath],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Execution timeout (30s)"
    except Exception as e:
        return 1, "", str(e)

def auto_fix_file(filepath, max_attempts=3):
    """Auto-fix a Python file by running it and fixing errors"""
    
    filepath = Path(filepath).resolve()
    
    if not filepath.exists():
        print(f"Err: File not found: {filepath}")
        return False
    
    print(f"\n[START] auto-fix for: {filepath.name}")
    print(f"Max attempts: {max_attempts}\n")
    
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        print(f"[Attempt {attempt}/{max_attempts}]")
        
        # Run the file
        return_code, stdout, stderr = run_python_file(str(filepath))
        
        if return_code == 0:
            print(f"SUCCESS! File executed without errors")
            if stdout:
                print(f"\nOutput:\n{stdout}")
            return True
        
        # Error occurred
        error_msg = stderr if stderr else stdout
        print(f"Error detected:")
        print(f"{error_msg[:200]}...")
        
        # Get current code
        current_code = read_file(filepath)
        
        # Get fix from Claude
        fixed_code = get_claude_fix(error_msg, filepath.name, current_code)
        
        # Apply fix
        print(f"Applying fix...")
        write_file(filepath, fixed_code)
        print(f"Code updated\n")
    
    print(f"Failed after {max_attempts} attempts")
    return False

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python auto_fix_with_claude.py <python_file>")
        print("\nExample: python auto_fix_with_claude.py upstox_auth.py")
        sys.exit(1)
    
    target_file = sys.argv[1]
    max_attempts = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    
    # Check API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("Error: ANTHROPIC_API_KEY not found in .env file")
        print("Please create .env file with your API key")
        sys.exit(1)
    
    success = auto_fix_file(target_file, max_attempts)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
