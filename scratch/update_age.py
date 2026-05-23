import os

files = [
    "terms.html",
    "rules.html",
    "knowledge-base.html",
    "jobs.html",
    "jobs-shifts.html",
    "jobs-one-time.html",
    "internships.html",
    "index.html",
    "employers.html"
]

target = "14–25"
replacement = "14–22"

for filename in files:
    filepath = os.path.join(r"d:\TeenWork", filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace(target, replacement)
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")
        else:
            print(f"No changes needed for {filename}")
    else:
        print(f"File {filename} not found")
