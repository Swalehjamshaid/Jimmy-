
# app/core/sitemap.py
import httpx
from urllib.parse import urljoin
import xml.etree.ElementTree as ET


def fetch_sitemap(base_url: str, robots_info: dict | None = None, timeout: int = 10) -> dict:
    urls = []
    candidates = []
    if robots_info:
        candidates.extend(robots_info.get('sitemaps', []))
    candidates.append(urljoin(base_url, '/sitemap.xml'))

    with httpx.Client(timeout=timeout) as client:
        for u in candidates[:5]:
            try:
                r = client.get(u, follow_redirects=True)
                if r.status_code == 200 and r.headers.get('content-type', '').lower().find('xml') != -1:
                    try:
                        root = ET.fromstring(r.text)
                        for loc in root.iter('{*}loc'):
                            if loc.text:
                                urls.append(loc.text.strip())
                        break
                    except Exception:
                        pass
            except Exception:
                pass
    return {"sources": candidates, "urls": urls[:200]}
