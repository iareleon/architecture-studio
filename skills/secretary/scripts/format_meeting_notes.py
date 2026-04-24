import sys
import os
import re

def format_file(file_path, is_script=False):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not is_script:
        content = re.sub(r'!\[unticked\]\(data:image/[^)]+\)', '[ ]', content)
        content = re.sub(r'-\s*-\s*\[ \]', '- [ ]', content)
        content = re.sub(r'-\s*\[\s*\]\s*\n+\s*(\[.*?\])', r'- [ ] \1', content)
    else:
        content = re.sub(r'^\*\*\s*\n*', '', content)
        content = re.sub(r'\n*\*\*\s*$', '', content)
        
    content = re.sub(r'^[ \t\xa0\u00a0]+$', '', content, flags=re.MULTILINE)
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip() + '\n'

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python format_meeting_notes.py <file_path> [--script]')
        sys.exit(1)
        
    file_path = sys.argv[1]
    is_script = len(sys.argv) > 2 and sys.argv[2] == '--script'
    
    if os.path.exists(file_path):
        format_file(file_path, is_script)
        print(f'Successfully formatted: {file_path}')
    else:
        print(f'File not found: {file_path}')