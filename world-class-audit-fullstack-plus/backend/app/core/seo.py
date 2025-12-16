
# app/core/seo.py
from bs4 import BeautifulSoup

def check_seo(html: str) -> dict:
    soup = BeautifulSoup(html, 'lxml')
    title = soup.title.string.strip() if soup.title and soup.title.string else ''
    meta_desc = ''
    md = soup.find('meta', attrs={'name': 'description'})
    if md and md.get('content'):
        meta_desc = md['content'].strip()
    h1 = soup.find('h1')
    canonical = soup.find('link', rel='canonical')
    robots = soup.find('meta', attrs={'name': 'robots'})
    ld_json = soup.find('script', type='application/ld+json') is not None
    og_title = soup.find('meta', property='og:title') is not None

    return {
        'title': title,
        'title_length': len(title),
        'meta_description': meta_desc,
        'meta_description_length': len(meta_desc),
        'has_h1': h1 is not None,
        'canonical': canonical.get('href') if canonical and canonical.get('href') else '',
        'robots': robots.get('content') if robots and robots.get('content') else '',
        'has_structured_data': ld_json,
        'has_og_title': og_title,
    }
