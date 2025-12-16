
# app/core/robots.py
import httpx
from urllib.parse import urljoin


def fetch_robots(base_url: str, timeout: int = 10) -> dict:
    url = urljoin(base_url, '/robots.txt')
    data = {"url": url, "present": False, "rules": [], "sitemaps": []}
    try:
        with httpx.Client(timeout=timeout) as client:
            r = client.get(url)
            if r.status_code == 200:
                data["present"] = True
                lines = r.text.splitlines()
                for line in lines:
                    s = line.strip()
                    if not s or s.startswith('#'):
                        continue
                    if s.lower().startswith('sitemap:'):
                        data["sitemaps"].append(s.split(':', 1)[1].strip())
                    else:
                        data["rules"].append(s)
    except Exception:
        pass
    return data
