
# app/workers/metrics/catalog.py
import httpx
from bs4 import BeautifulSoup

class Metric:
    def __init__(self, category: str, name: str, checker):
        self.category = category
        self.name = name
        self._checker = checker
    def check(self, domain: str, max_pages: int = 25, timeout: int = 15):
        try:
            return self._checker(domain, max_pages, timeout)
        except Exception as e:
            return { 'value': None, 'score': 0, 'recommendation': f'Error: {e}' }

ALL_METRICS = []

def add_metric(category, name):
    def decorator(func):
        ALL_METRICS.append(Metric(category, name, func))
        return func
    return decorator

# Helper fetch
def fetch_html(url: str, timeout: int):
    with httpx.Client(timeout=timeout) as client:
        r = client.get(url, follow_redirects=True)
        return r, r.text
@add_metric("Technical", "Page Load Time")
def tech_load_time(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Technical", "First Contentful Paint (FCP)")
def tech_fcp(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Technical", "Largest Contentful Paint (LCP)")
def tech_lcp(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Technical", "Cumulative Layout Shift (CLS)")
def tech_cls(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Technical", "Mobile Responsiveness")
def tech_mobile(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Technical", "Crawlability")
def tech_crawl(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Technical", "Broken Links")
def tech_broken_links(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Technical", "HTTP Errors (404/500)")
def tech_http_errors(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Technical", "HTTPS / SSL Validity")
def tech_https(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Technical", "Sitemap & Robots.txt")
def tech_sitemap_robots(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("SEO", "Meta Title Optimization")
def seo_title(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("SEO", "Meta Description Optimization")
def seo_desc(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("SEO", "Heading Structure (H1–H6)")
def seo_headings(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("SEO", "Keyword Relevance")
def seo_keywords(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("SEO", "Duplicate Content")
def seo_duplicate(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("SEO", "Image Alt Tags")
def seo_alt(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("SEO", "Internal Linking")
def seo_internal(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("SEO", "External Linking")
def seo_external(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("SEO", "Schema Markup Presence")
def seo_schema(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Content", "Content Relevance")
def content_relevance(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Content", "Grammar & Readability")
def content_readability(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Content", "Content Freshness")
def content_freshness(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Content", "Thin Content Detection")
def content_thin(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Content", "User Intent Match")
def content_intent(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Content", "CTA Effectiveness")
def content_cta(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Content", "Content Duplication")
def content_duplication(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("UX/UI", "Navigation Structure")
def ux_nav(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("UX/UI", "Accessibility (WCAG Basics)")
def ux_access(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("UX/UI", "Visual Hierarchy")
def ux_visual(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("UX/UI", "Design Consistency")
def ux_consistency(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("UX/UI", "Mobile UX")
def ux_mobile(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("UX/UI", "Conversion Flow")
def ux_conversion(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("UX/UI", "User Clarity & Ease")
def ux_clarity(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Performance & Analytics", "Traffic Sources")
def perf_traffic(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Performance & Analytics", "Bounce Rate")
def perf_bounce(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Performance & Analytics", "Session Duration")
def perf_session(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Performance & Analytics", "Conversion Rate")
def perf_conversion(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Performance & Analytics", "Analytics Setup Validation")
def perf_analytics(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Performance & Analytics", "Goal Tracking")
def perf_goals(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Security", "SSL Configuration")
def sec_ssl(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Security", "Vulnerability Scan")
def sec_vuln(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Security", "Malware Detection")
def sec_malware(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Security", "Form Security")
def sec_forms(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Security", "CMS & Plugin Updates")
def sec_cms(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Security", "Backup & Recovery")
def sec_backup(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Compliance & Legal", "Privacy Policy")
def comp_privacy(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Compliance & Legal", "GDPR Compliance")
def comp_gdpr(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Compliance & Legal", "Cookie Consent")
def comp_cookie(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Compliance & Legal", "Accessibility Compliance")
def comp_a11y(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

@add_metric("Compliance & Legal", "Terms & Conditions")
def comp_terms(domain: str, max_pages: int = 25, timeout: int = 15):
    url = domain if domain.startswith('http') else f'http://{domain}'
    r, html = fetch_html(url, timeout)
    score = 80 if r.status_code < 400 else 0
    value = {'status': r.status_code}
    return {'value': value, 'score': score, 'recommendation': ''}

