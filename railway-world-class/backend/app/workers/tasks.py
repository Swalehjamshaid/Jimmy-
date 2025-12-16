
import os, subprocess, json

def find_chrome():
       path = os.getenv("CHROME_PATH", "/usr/bin/chromium")
    return path if os.path.exists(path) else None

def run_lighthouse(url: str) -> dict:
    chrome = find_chrome()
    cmd = [
        "lighthouse", url,
        "--quiet", "--output=json", "--only-categories=performance",
        "--chrome-flags=--headless --no-sandbox"
    ]
    if chrome:
        cmd.append(f"--chrome-path={chrome}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return {}
    try:
        return json.loads(res.stdout)
    except:
