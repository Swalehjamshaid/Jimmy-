
# app/core/security.py
from typing import Dict, List
from urllib.parse import urlparse
from bs4 import BeautifulSoup

REQUIRED_HEADERS = [
    "content-security-policy",
    "strict-transport-security",
    "x-frame-options",
    "x-content-type-options",
    "referrer-policy",
    "permissions-policy",
]

RECOMMENDED_VALUES = {
    "x-content-type-options": "nosniff",
    "x-frame-options": ["DENY", "SAMEORIGIN"],
}


def check_security_headers(headers: Dict[str, str]) -> Dict:
    out = {"missing": [], "present": {}, "recommendations": []}
    lower = {k.lower(): v for k, v in headers.items()}
    for h in REQUIRED_HEADERS:
        if h in lower:
            out["present"][h] = lower[h]
        else:
            out["missing"].append(h)
    for h, val in RECOMMENDED_VALUES.items():
        cur = lower.get(h)
        if cur is None:
            out["recommendations"].append(f"Add {h}: {val}")
        else:
            if isinstance(val, list) and cur not in val:
                out["recommendations"].append(f"Set {h} to one of {val}; current='{cur}'")
            elif isinstance(val, str) and cur.strip().lower() != val:
                out["recommendations"].append(f"Set {h} to '{val}'; current='{cur}'")
    return out


def check_https_enforcement(url: str, final_url: str, headers: Dict[str, str], html: str) -> Dict:
    """Checks if site enforces HTTPS and flags mixed content on HTTPS pages."""
    res = {"initial_scheme": urlparse(url).scheme, "final_scheme": urlparse(final_url).scheme,
           "hsts": False, "mixed_content": []}
    lower = {k.lower(): v for k, v in headers.items()}
    hsts = lower.get('strict-transport-security')
    res["hsts"] = bool(hsts)

    # Mixed content scan
    if urlparse(final_url).scheme == 'https':
        soup = BeautifulSoup(html, 'lxml')
        http_resources: List[str] = []
        for attr in ['src', 'href']:
            for tag in soup.find_all(attrs={attr: True}):
                val = tag.get(attr)
                if isinstance(val, str) and val.strip().lower().startswith('http://'):
                    http_resources.append(val)
        res["mixed_content"] = list(dict.fromkeys(http_resources))[:50]
    return res
