import os
import re

cwd = os.getcwd()

# 1. Delete the files
files_to_delete = ['insurance.html', 'pro.html']
for f in files_to_delete:
    path = os.path.join(cwd, f)
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted {f}")

# 2. Patterns to remove from HTML files
# We want to remove the <li> containing the link
patterns = [
    re.compile(r'<li><a href="pro\.html">.*?</a></li>\s*', re.IGNORECASE),
    re.compile(r'<li><a href="insurance\.html">.*?</a></li>\s*', re.IGNORECASE)
]

html_files = [f for f in os.listdir(cwd) if f.endswith('.html')]

for filename in html_files:
    path = os.path.join(cwd, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    for pattern in patterns:
        content = pattern.sub('', content)
    
    if content != original_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated links in {filename}")

# 3. Update update_buttons.py
update_buttons_path = os.path.join(cwd, 'update_buttons.py')
if os.path.exists(update_buttons_path):
    with open(update_buttons_path, 'r', encoding='utf-8') as f:
        ub_content = f.read()
    
    # Remove pro.html and insurance.html from the list
    ub_content = ub_content.replace("'pro.html', ", "")
    ub_content = ub_content.replace("'insurance.html', ", "")
    ub_content = ub_content.replace(", 'insurance.html'", "") # in case it's at the end
    
    with open(update_buttons_path, 'w', encoding='utf-8') as f:
        f.write(ub_content)
    print("Updated update_buttons.py")

# 4. Update generate_pages.py (if it exists)
generate_pages_path = os.path.join(cwd, 'generate_pages.py')
if os.path.exists(generate_pages_path):
    # This might be tricky if it's a large dict. 
    # Let's just remove the keys manually if we can identify them.
    # For now, let's at least try the simple replacement.
    pass
