
from typing import Callable, Dict, Any, List
import httpx, ssl, socket
MetricFn = Callable[[str], Dict[str, Any]]
REGISTRY: List[Dict[str, Any]] = []

def register(category: str, name: str, fn: MetricFn):
    REGISTRY.append({"category": category, "name": name, "fn": fn})

async def fetch_status(url: str) -> int:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(url)
            return r.status_code
    except:
        return 0

async def https_ssl(domain: str):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                ssock.getpeercert()
        return {"value": "valid", "score": 100.0, "recommendation": "SSL valid"}
    except:
        return {"value": "invalid", "score": 20.0, "recommendation": "Fix SSL"}

register("Technical", "HTTPS / SSL Validity", https_ssl)
