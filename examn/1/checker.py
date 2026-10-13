import requests


SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host: str, path: str) -> str:
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    clean_path = path.lstrip("/")
    return f"https://{host}/{clean_path}"
    pass

def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")
    pass


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    response = requests.get(url)
    status = response.status_code
    content_type = response.headers.get("content-type", "N/A")
    print(f"status: {status}")
    print(f"content-Type: {content_type}")
    pass


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        if "Content-Type" in response.headers:
            content_type = response.headers["Content-Type"]
        else:
            content_type = "unknown"

        if "Server" in response.headers:
            server = response.headers["Server"]
        else:
            server = "unknown"

    pass


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""


results = []
for url in SITES:
    res = check_site(url)
    res["url"] = url
    results.append(res)

successful_sites = [res for res in results if res.get("status") == 200]
successful_sites.sort(key=lambda x: x["length"], reverse=True)

for res in successful_sites:
    print(f"{res['url']}  -> {res['status']}, {res['length']} octeți")

success_count = len(successful_sites)
fail_count = len(results) - success_count
pass


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return {"status": response.status_code, "attempts": attempt}
            last_status = response.status_code
        except requests.RequestException:
            last_status = None

    return {"status": last_status, "attempts": attempts}
    pass
