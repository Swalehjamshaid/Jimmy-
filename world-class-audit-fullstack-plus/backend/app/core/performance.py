
# app/core/performance.py
import time
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def measure_ttfb(url: str, timeout: int = 15) -> float:
    start = time.perf_counter()
    with httpx.Client(timeout=timeout) as client:
        r = client.get(url, follow_redirects=True)
    return (time.perf_counter() - start) * 1000.0


def count_resources(html: str) -> dict:
    soup = BeautifulSoup(html, 'lxml')
    return {
        'scripts': len(soup.find_all('script')),
        'stylesheets': len(soup.find_all('link', rel='stylesheet')),
        'images': len(soup.find_all('img')),
    }


def resource_bytes(html: str, base_url: str, timeout: int = 10) -> int:
    """Try to sum sizes of linked JS/CSS/images via HEAD (Content-Length)."""
    soup = BeautifulSoup(html, 'lxml')
    urls = []
    for tag in soup.find_all(['script', 'link', 'img']):
        u = tag.get('src') or (tag.get('href') if tag.name == 'link' else None)
        if u:
            urls.append(urljoin(base_url, u))
    total = 0
    with httpx.Client(timeout=timeout) as client:
        for u in urls[:50]:
            try:
                r = client.head(u, follow_redirects=True)
                cl = r.headers.get('content-length')
                if cl and cl.isdigit():
                    total += int(cl)
            except Exception:
                pass
    return total
