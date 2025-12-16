
# app/core/links.py
import httpx
from bs4 import BeautifulSoup
from .utils import normalize_url


def check_links(html: str, base_url: str, timeout: int = 10):
    """Return broken links list: [(url, status or error)]."""
    soup = BeautifulSoup(html, 'lxml')
    hrefs = [a.get('href') for a in soup.select('a[href]')]
    urls = [normalize_url(base_url, h) for h in hrefs if h]
    broken = []
    with httpx.Client(timeout=timeout) as client:
        for u in urls[:100]:
            try:
                r = client.get(u, follow_redirects=True)
                if r.status_code >= 400:
                    broken.append((u, r.status_code))
            except Exception as e:
                broken.append((u, str(e)))
    return broken
