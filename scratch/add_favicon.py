import os
import re

def add_favicon(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    favicon_tag = '<link rel="icon" type="image/jpeg" href="favicon.jpeg">'
    
    # Check if favicon already exists (standard link rel="icon")
    if 'favicon.jpeg' in content and 'rel="icon"' in content:
        # Already has it, maybe check if it needs update or skip
        return
    
    # Remove existing favicon tags to avoid duplicates
    content = re.sub(r'<link rel="(?:shortcut )?icon"[^>]*>', '', content)
    
    # Insert before </head>
    if '</head>' in content:
        content = content.replace('</head>', f'    {favicon_tag}\n</head>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Favicon added to: {filepath}")

def main():
    skip_dirs = {'.git', 'node_modules', 'backend'} # Skip backend just in case
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for file in files:
            if file.endswith('.html'):
                add_favicon(os.path.join(root, file))

if __name__ == '__main__':
    main()
