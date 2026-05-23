# -*- coding: utf-8 -*-
import os
import re

# Mapping for image localization
IMAGE_MAP = {
    'https://ui-avatars.com/api/?name=TechNova&background=random': 'assets/загрузка.svg',
    'https://ui-avatars.com/api/?name=CodeCraft&background=random': 'assets/загрузка (1).svg',
    'https://ui-avatars.com/api/?name=CreativeFlow&background=random': 'assets/загрузка (2).svg',
    'https://ui-avatars.com/api/?name=EcoStyle&background=random': 'assets/загрузка (3).svg',
    'https://ui-avatars.com/api/?name=SmartEdu&background=random': 'assets/загрузка (4).svg',
    'https://ui-avatars.com/api/?name=ActiveLife&background=random': 'assets/загрузка (5).svg',
    'https://ui-avatars.com/api/?name=FoodExpress&background=random': 'assets/загрузка (6).svg',
    'https://ui-avatars.com/api/?name=ClickMedia&background=random': 'assets/загрузка (7).svg',
    'https://ui-avatars.com/api/?name=FashionLab&background=random': 'assets/загрузка (8).svg',
    'https://ui-avatars.com/api/?name=PetsCare&background=random': 'assets/загрузка (9).svg',
}

def remove_google_fonts(content):
    # Remove standard Google Fonts links and preconnect tags
    content = re.sub(r'\s*<link\s+rel="preconnect"\s+href="https://fonts\.googleapis\.com"\s*\/?>', '', content)
    content = re.sub(r'\s*<link\s+rel="preconnect"\s+href="https://fonts\.gstatic\.com"\s+crossorigin\s*\/?>', '', content)
    
    # Remove google fonts css link (single or multi-line)
    content = re.sub(r'\s*<link\s+href="https://fonts\.googleapis\.com/css2\?[^"]+"\s+rel="stylesheet"\s*\/?>', '', content)
    content = re.sub(r'\s*<link\s+rel="stylesheet"\s+href="https://fonts\.googleapis\.com/css2\?[^"]+"\s*\/?>', '', content)
    content = re.sub(r'\s*<link\s+href="https://fonts\.googleapis\.com/css2\?[^"]+"\s*\n?\s*rel="stylesheet"\s*\/?>', '', content)
    
    # Fallback to catch any remaining google fonts references in link tags
    content = re.sub(r'\s*<link\s+[^>]*href="https://fonts\.googleapis\.com[^>]*>', '', content, flags=re.DOTALL)
    content = re.sub(r'\s*<link\s+[^>]*href="https://fonts\.gstatic\.com[^>]*>', '', content, flags=re.DOTALL)
    
    return content

def fix_footer(content):
    if 'footer-links' in content:
        return content  # Already has the footer links
    
    footer_links_addition = """
                <div class="footer-links">
                    <h4 class="footer-title">Платформа</h4>
                    <ul>
                        <li><a href="employers.html">Для работодателей</a></li>
                    </ul>
                </div>

                <div class="footer-links">
                    <h4 class="footer-title">Поддержка</h4>
                    <ul>
                        <li><a href="knowledge-base.html">База знаний</a></li>
                        <li><a href="Политика конфиденциальности TeenWork.pdf" target="_blank">Политика конфиденциальности</a></li>
                        <li><a href="Публичная оферта (Пользовательское соглашение) платформы TeenWork.pdf" target="_blank">Пользовательское соглашение</a></li>
                    </ul>
                </div>
            <div class="fz-disclaimer">
                Данный сайт является некоммерческим прототипом. Сбор и обработка персональных данных не осуществляются. 
                Все вводимые данные используются только для демонстрации интерфейса и не сохраняются.
            </div>"""
            
    if '<div class="footer-bottom">' in content:
        content = content.replace('<div class="footer-bottom">', footer_links_addition + '\n            <div class="footer-bottom">')
    return content

def apply_all():
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    print(f"Found {len(html_files)} HTML files to process.")
    
    for file in html_files:
        print(f"Processing: {file}")
        
        # 1. Read file as UTF-8 first
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file, 'r', encoding='cp1251') as f:
                content = f.read()
                
        # 2. Localize external avatars
        # Replace i.pravatar.cc links
        content = re.sub(r'https://i\.pravatar\.cc/\d+\?img=\d+', 'assets/150.jpg', content)
        content = re.sub(r'https://i\.pravatar\.cc/\d+', 'assets/150.jpg', content)
        
        # Replace ui-avatars links using the mapping
        for external_url, local_path in IMAGE_MAP.items():
            content = content.replace(external_url, local_path)
            
        # Fallback regex for remaining ui-avatars
        content = re.sub(r'https://ui-avatars\.com/api/\?[^"\']+', 'assets/загрузка.svg', content)
        
        # 3. Remove Google Fonts links
        content = remove_google_fonts(content)
        
        # 4. Apply file-specific modifications
        if file == 'auth.html':
            # Checkbox consent replacements
            old_consent = '<div style="text-align: left; margin-bottom: 24px; font-size: 0.85rem; color: var(--text-muted);">\n                    Нажимая «Зарегистрироваться», вы соглашаетесь с <a href="Публичная оферта (Пользовательское соглашение) платформы TeenWork.pdf" target="_blank" style="color: var(--primary);">Пользовательским соглашением</a>.\n                </div>'
            # Also handle variant formatting
            old_consent_alt = 'Нажимая «Зарегистрироваться», вы соглашаетесь с <a href="Публичная оферта (Пользовательское соглашение) платформы TeenWork.pdf" target="_blank" style="color: var(--primary);">Пользовательским соглашением</a>.'
            
            new_consent = """<div style="text-align: left; margin-bottom: 24px; font-size: 0.85rem; color: var(--text-muted);">
                    <div style="display: flex; align-items: flex-start; gap: 8px; margin-bottom: 12px;">
                        <input type="checkbox" id="agree-terms" required style="margin-top: 4px;">
                        <label for="agree-terms" style="cursor: pointer;">Я ознакомился(-лась) и принимаю условия <a href="Публичная оферта (Пользовательское соглашение) платформы TeenWork.pdf" target="_blank" style="color: var(--primary);">Пользовательского соглашения</a></label>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 8px; margin-bottom: 12px;">
                        <input type="checkbox" id="agree-privacy" required style="margin-top: 4px;">
                        <label for="agree-privacy" style="cursor: pointer;">Я даю согласие на обработку моих персональных данных в соответствии с <a href="Политика конфиденциальности TeenWork.pdf" target="_blank" style="color: var(--primary);">Политикой конфиденциальности</a></label>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 8px;">
                        <input type="checkbox" id="agree-parent" style="margin-top: 4px;">
                        <label for="agree-parent" style="cursor: pointer;">Я подтверждаю, что мой законный представитель (родитель/опекун) уведомлён о моей регистрации на платформе и даёт согласие на обработку моих персональных данных (для пользователей 14–17 лет)</label>
                    </div>
                </div>"""
                
            if old_consent in content:
                content = content.replace(old_consent, new_consent)
            elif old_consent_alt in content:
                content = content.replace(old_consent_alt, new_consent)
            else:
                # Regex based fallback replacement
                content = re.sub(r'Нажимая «Зарегистрироваться».*?Пользовательским соглашением</a>\.', new_consent, content)
                
        elif file == 'partnership.html':
            # Add consent text below partnership-form
            old_form = '</form>'
            new_form_consent = """</form>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 10px; text-align: left;">
                    Отправляя email, вы даете согласие на обработку персональных данных в соответствии с <a href="Политика конфиденциальности TeenWork.pdf" target="_blank" style="color: var(--primary);">Политикой конфиденциальности</a>.
                </div>"""
            
            # Replace the first occurrence of </form> in partnership-form
            content = content.replace('id="partnership-form">\n                    <input type="email" class="btn btn-outline" style="background: white; flex: 1; text-align: left; cursor: text;" placeholder="Ваш Email" required>\n                    <button type="submit" class="btn btn-primary">Отправить</button>\n                </form>', 
                                      'id="partnership-form">\n                    <input type="email" class="btn btn-outline" style="background: white; flex: 1; text-align: left; cursor: text;" placeholder="Ваш Email" required>\n                    <button type="submit" class="btn btn-primary">Отправить</button>\n                ' + new_form_consent)
            
        elif file == 'secret-teen-dashboard.html':
            # Account deletion block
            deletion_block = """
                <!-- ========== ACCOUNT SETTINGS (152-FZ) ========== -->
                <div class="dash-card full-width" id="account-settings">
                    <div class="dash-card-header">
                        <div class="dash-card-title">
                            <i class="ph-duotone ph-gear"></i>
                            Управление аккаунтом
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 16px;">
                        <p style="font-size: 0.9rem; color: var(--text-muted);">
                            В соответствии со ст. 21 Федерального закона от 27.07.2006 N 152-ФЗ «О персональных данных», вы имеете право потребовать полного удаления вашего аккаунта и всех связанных с ним персональных данных.
                        </p>
                        <div>
                            <button class="btn btn-outline" style="color: #ef4444; border-color: rgba(239, 68, 68, 0.3);" onclick="confirm('Вы уверены, что хотите безвозвратно удалить свой аккаунт? Все ваши данные, отзывы и история будут удалены.')">
                                <i class="ph-duotone ph-trash"></i> Удалить аккаунт
                            </button>
                        </div>
                    </div>
                </div>
            """
            
            # Place it right before `</div><!-- /dashboard-grid -->`
            content = content.replace('</div><!-- /dashboard-grid -->', deletion_block + '\n            </div><!-- /dashboard-grid -->')
            
        elif file == 'secret-parent-dashboard.html':
            # Account deletion block
            deletion_block = """
                <!-- ========== ACCOUNT SETTINGS (152-FZ) ========== -->
                <div class="dash-card full-width" id="account-settings">
                    <div class="dash-card-header">
                        <div class="dash-card-title">
                            <i class="ph-duotone ph-gear"></i>
                            Управление аккаунтом
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 16px;">
                        <p style="font-size: 0.9rem; color: var(--text-muted);">
                            В соответствии со ст. 21 Федерального закона от 27.07.2006 N 152-ФЗ «О персональных данных», вы имеете право потребовать полного удаления вашего аккаунта и связанных данных (включая привязанные аккаунты детей, если они не достигли 18 лет).
                        </p>
                        <div>
                            <button class="btn btn-outline" style="color: #ef4444; border-color: rgba(239, 68, 68, 0.3);" onclick="confirm('Вы уверены, что хотите удалить аккаунт родителя? Это действие также может заблокировать доступ для привязанных детских аккаунтов, требующих согласия.')">
                                <i class="ph-duotone ph-trash"></i> Удалить аккаунт
                            </button>
                        </div>
                    </div>
                </div>
            """
            
            # Place it right before `</div><!-- /dashboard-grid -->`
            content = content.replace('</div><!-- /dashboard-grid -->', deletion_block + '\n            </div><!-- /dashboard-grid -->')
            
        # 5. Fix/add footer links and disclaimer
        content = fix_footer(content)
        
        # 6. Save as UTF-8
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("Encoding conversion and 152-FZ compliance modifications completed successfully!")

if __name__ == "__main__":
    apply_all()
