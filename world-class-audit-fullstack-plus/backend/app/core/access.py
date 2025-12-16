
# app/core/access.py
from bs4 import BeautifulSoup

def check_accessibility(html: str) -> dict:
    soup = BeautifulSoup(html, 'lxml')
    imgs = soup.find_all('img')
    images_without_alt = [img.get('src') for img in imgs if not img.get('alt')]
    html_tag = soup.find('html')
    lang_attr = html_tag.get('lang') if html_tag else None
    labels = soup.find_all('label')
    inputs = soup.find_all('input')
    labeled_inputs = sum(1 for i in inputs if i.get('id') and soup.find('label', attrs={'for': i.get('id')}))
    return {
        'images_without_alt_count': len(images_without_alt),
        'images_without_alt': images_without_alt[:20],
        'has_lang_attribute': bool(lang_attr),
        'label_to_input_ratio': (labeled_inputs, len(inputs)),
    }
