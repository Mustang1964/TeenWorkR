import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to find social link anchor tags without target="_blank"
    # and add target="_blank" rel="noopener noreferrer"
    
    # We want to target links inside .social-links div mostly, but since the request is general...
    # Let's find specific hrefs we know are social links
    
    social_hrefs = [
        r'https://t\.me/teenWoork',
        r'https://vk\.ru/club237616752',
        r'https://www\.tiktok\.com/@teenwork_official\?_r=1&_t=ZS-95Xkn41rAJT'
    ]
    
    changed = False
    for href in social_hrefs:
        # Check if already has target="_blank"
        pattern = re.compile(rf'<a\s+href="{href}"(?![^>]*target="_blank")')
        if pattern.search(content):
            content = pattern.sub(f'<a href="{href}" target="_blank" rel="noopener noreferrer"', content)
            changed = True
            
    # Also handle the MAX link which is often href="#" but labeled MAX
    pattern_max = re.compile(r'<a\s+href="#"(?![^>]*target="_blank")(?=[^>]*aria-label="MAX")')
    if pattern_max.search(content):
        content = pattern_max.sub('<a href="#" target="_blank" rel="noopener noreferrer"', content)
        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")

def main():
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                fix_file(os.path.join(root, file))

if __name__ == '__main__':
    main()
