import os
import re

files_to_update = [
    'terms.html', 'rules.html', 'pro.html', 'knowledge-base.html', 'jobs.html',
    'jobs-shifts.html', 'jobs-one-time.html', 'internships.html', 'insurance.html',
    'index.html', 'employers.html'
]

dir_path = 'd:\\TeenWork'

for filename in files_to_update:
    filepath = os.path.join(dir_path, filename)
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update <button> to <a> for btn-register
    content = re.sub(
        r'<button class="btn btn-primary" id="btn-register">Зарегистрироваться</button>',
        r'<a href="auth.html?tab=register" class="btn btn-primary" id="btn-register" style="text-decoration:none;">Зарегистрироваться</a>',
        content
    )
    
    # Update <a> specifically if it's already an <a> but needs tab=register
    content = re.sub(
        r'<a href="auth.html" class="btn btn-primary" id="btn-register"',
        r'<a href="auth.html?tab=register" class="btn btn-primary" id="btn-register"',
        content
    )

    # Similarly for btn-login to make them links too
    content = re.sub(
        r'<button class="btn btn-outline" id="btn-login">Войти</button>',
        r'<a href="auth.html" class="btn btn-outline" id="btn-login" style="text-decoration:none;">Войти</a>',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated buttons to links with tab parameter.")
