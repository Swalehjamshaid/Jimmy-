
# app/core/audit.py
from typing import Dict, Any
from .crawler import Crawler
from .security import check_security_headers, check_https_enforcement
from .seo import check_seo
from .access import check_accessibility
from .performance import measure_ttfb, count_resources, resource_bytes
from .links import check_links
from .robots import fetch_robots
from .sitemap import fetch_sitemap
from .utils import origin


def run_audit(url: str, max_pages: int = 25, timeout: int = 15) -> Dict[str, Any]:
    crawler = Crawler(url, max_pages=max_pages, timeout=timeout)
    pages = crawler.run()

    base = origin(url)
    robots_info = fetch_robots(base, timeout=timeout)
    sitemap_info = fetch_sitemap(base, robots_info, timeout=timeout)

    summary = {
        'total_pages': len(pages),
        'ok_responses': sum(1 for p in pages.values() if isinstance(p.get('status'), int) and 200 <= p['status'] < 400),
        'errors': {u: p.get('error') for u, p in pages.items() if p.get('error')},
        'robots': robots_info,
        'sitemap': {'count': len(sitemap_info.get('urls', []))},
    }

    reports = {}
    for u, p in pages.items():
        if p.get('error'):
            continue
        headers = p.get('headers', {})
        html = p.get('content', '')
        sec = check_security_headers(headers)
        https = check_https_enforcement(url, p.get('final_url', url), headers, html)
        seo = check_seo(html)
        acc = check_accessibility(html)
        perf = {
            'ttfb_ms': measure_ttfb(u, timeout),
            'resources': count_resources(html),
            'page_weight_bytes_est': resource_bytes(html, u, timeout)
        }
        broken = check_links(html, u, timeout)
        reports[u] = {
            'status': p.get('status'),
            'security': sec,
            'https': https,
            'seo': seo,
            'accessibility': acc,
            'performance': perf,
            'broken_links': broken[:50],
        }
    return {'summary': summary, 'pages': reports, 'sitemap': sitemap_info}
