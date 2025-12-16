
# app/core/crawler.py
import httpx
from bs4 import BeautifulSoup
from .utils import normalize_url, same_domain

class Crawler:
    def __init__(self, start_url: str, max_pages: int = 25, timeout: int = 15):
        self.start_url = start_url
        self.max_pages = max_pages
        self.timeout = timeout
        self.visited = set()
        self.to_visit = [start_url]
        self.pages = {}

    def fetch(self, client: httpx.Client, url: str):
        try:
            resp = client.get(url, follow_redirects=True)
            content = resp.text
            return resp, content
        except Exception as e:
            return None, str(e)

    def run(self):
        with httpx.Client(timeout=self.timeout) as client:
            while self.to_visit and len(self.visited) < self.max_pages:
                url = self.to_visit.pop(0)
                if url in self.visited:
                    continue
                self.visited.add(url)
                resp, content = self.fetch(client, url)
                if resp is None:
                    self.pages[url] = {"error": content}
                    continue
                self.pages[url] = {
                    "status": resp.status_code,
                    "headers": dict(resp.headers),
                    "content": content,
                    "url": str(resp.url),
                    "final_url": str(resp.url),
                }
                soup = BeautifulSoup(content, 'lxml')
                for a in soup.select('a[href]'):
                    href = a.get('href')
                    nxt = normalize_url(str(resp.url), href)
                    if nxt and same_domain(self.start_url, nxt) and nxt not in self.visited:
                        self.to_visit.append(nxt)
        return self.pages
