
# app/core/utils.py
from urllib.parse import urljoin, urlparse

def origin(url: str) -> str:
    p = urlparse(url)
    return f"{p.scheme}://{p.netloc}"

def normalize_url(base: str, href: str) -> str:
    if not href:
        return ''
    href = href.strip()
    return urljoin(base, href)

def same_domain(url1: str, url2: str) -> bool:
    p1 = urlparse(url1)
    p2 = urlparse(url2)
    return p1.netloc == p2.netloc

def is_https(url: str) -> bool:
    return urlparse(url).scheme == 'https'
