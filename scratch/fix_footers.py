import os
import re

cwd = os.getcwd()
index_path = os.path.join(cwd, 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

social_pattern = re.compile(r'<div class="social-links">.*?</div>', re.DOTALL)
social_match = social_pattern.search(index_content)
if not social_match:
    print("Error: Could not find social-links in index.html")
    exit(1)
social_block = social_match.group(0).strip()

html_files = [f for f in os.listdir(cwd) if f.endswith('.html') and f != 'index.html']

for filename in html_files:
    file_path = os.path.join(cwd, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Remove all existing social-links blocks from this file to start clean
    content = social_pattern.sub('', content)
    
    # 2. Try to find the footer
    footer_match = re.search(r'<footer[^>]*>.*?</footer>', content, re.DOTALL)
    if footer_match:
        footer_content = footer_match.group(0)
        
        # Try to find a container inside the footer
        container_match = re.search(r'<div class="container">', footer_content)
        if container_match:
            # We have a container. 
            # Try to find footer-brand
            brand_match = re.search(r'<div class="footer-brand">', footer_content)
            if brand_match:
                # Insert after footer-desc if it exists inside brand, or after brand start
                desc_match = re.search(r'<p class="footer-desc">.*?</p>', footer_content, re.DOTALL)
                if desc_match:
                    new_footer = footer_content.replace(desc_match.group(0), desc_match.group(0) + '\n                    ' + social_block)
                else:
                    new_footer = footer_content.replace('<div class="footer-brand">', '<div class="footer-brand">\n                    ' + social_block)
            else:
                # No brand, insert at the beginning of the container
                new_footer = footer_content.replace('<div class="container">', '<div class="container">\n                ' + social_block)
            
            content = content.replace(footer_content, new_footer)
            print(f"Fixed footer in {filename}")
        else:
            # Simple footer without container?
            new_footer = footer_content.replace('<footer', '<footer') # just a placeholder
            # Insert before last </footer>
            content = content.replace('</footer>', '\n            ' + social_block + '\n        </footer>', 1)
            print(f"Added to footer-end in {filename}")
    else:
        # No footer? Maybe auth.html. Let's just not add it if there's no footer, 
        # or add it at the bottom. User said "in all footers".
        print(f"No footer found in {filename}, skipping.")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
