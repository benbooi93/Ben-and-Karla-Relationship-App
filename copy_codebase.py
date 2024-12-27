import os
import pyperclip
from datetime import datetime

def copy_codebase_to_clipboard():
    # List of relevant files
    relevant_files = [
        'test_twilio_call.py',
        'webhook_server.py',
        'requirements.txt',
        'simple_caller.py',
        'app.py',
        '.env',
        'restaurant_caller.py',
        'README.md',
        'websocket_server.py',
        'ngrok.yml',
        'dev'
    ]
    
    codebase = []
    
    # Add title and timestamp
    codebase.append("# AI Phone Call System Codebase")
    codebase.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Add files in the specified order
    for filename in relevant_files:
        if os.path.exists(filename):
            # Add file header
            codebase.append(f"\n{'='*80}")
            codebase.append(f"File: {filename}")
            codebase.append('='*80 + '\n')
            
            # Read and add file contents
            try:
                with open(filename, 'r') as f:
                    codebase.append(f.read())
            except Exception as e:
                codebase.append(f"Error reading file: {str(e)}")
        else:
            print(f"⚠️ Warning: File not found: {filename}")
    
    # Join all content and copy to clipboard
    full_content = '\n'.join(codebase)
    pyperclip.copy(full_content)
    
    # Print summary
    print("\n✅ Codebase copied to clipboard")
    print(f"📊 Stats:")
    print(f"  • {len(full_content):,} characters")
    print(f"  • {sum(1 for line in full_content.split('\n')):,} lines")
    print(f"  • {sum(1 for f in relevant_files if os.path.exists(f))} files copied")
    print(f"  • {sum(1 for f in relevant_files if not os.path.exists(f))} files missing")

if __name__ == "__main__":
    copy_codebase_to_clipboard() 