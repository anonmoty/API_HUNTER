import requests
from urllib.parse import urlparse
from core.colors import C
from core.config import Config

class APIVersioning:
    name = "API Version Discovery"

    def __init__(self, url):
        self.url = url
        self.apis = []

    def run(self):
        print("\n" + C.B + "=" * 62 + C.RESET)
        print("  " + C.BOLD + C.G + "[12/12] API VERSION DISCOVERY" + C.RESET)
        print(C.B + "=" * 62 + C.RESET)

        base = self.url.rstrip("/")
        versions = [
            "/api/v1", "/api/v2", "/api/v3", "/api/v4", "/api/v5",
            "/api/v0.1", "/api/v0.9", "/api/v1.0", "/api/v1.1",
            "/api/v2.0", "/api/v2.1", "/api/v3.0",
            "/v1", "/v2", "/v3", "/v4", "/v5",
            "/api/1.0", "/api/2.0", "/api/3.0",
            "/api/beta", "/api/alpha", "/api/latest", "/api/stable",
            "/api/internal", "/api/external", "/api/deprecated",
            "/api/legacy", "/api/new", "/api/old",
        ]

        print("  " + C.info("Testing " + str(len(versions)) + " version paths..."))
        for v in versions:
            test_url = base + v
            try:
                resp = requests.get(test_url, timeout=5, headers=Config.HEADERS, allow_redirects=False)
                if resp.status_code in [200, 301, 302, 401, 403]:
                    self.apis.append(test_url)
                    ct = resp.headers.get("Content-Type", "")[:30]
                    color = C.G if resp.status_code == 200 else C.Y
                    print("    " + color + "[" + str(resp.status_code) + "]" + C.RESET + " " + test_url + " " + C.D + ct + C.RESET)
            except Exception:
                pass

        # Header-based versioning
        print("\n  " + C.info("Testing header-based versioning..."))
        version_headers = {
            "Accept": "application/vnd.api+json;version=2",
            "X-API-Version": "2",
            "Api-Version": "2024-01-01",
        }
        for header, val in version_headers.items():
            try:
                h = dict(Config.HEADERS)
                h[header] = val
                resp = requests.get(base + "/api", headers=h, timeout=5)
                if resp.status_code == 200:
                    print("    " + C.warn("Header versioning: " + header + ": " + val))
            except Exception:
                pass

        self.apis = list(set(self.apis))
        print("\n  " + C.BOLD + C.G + "[+] API versions: " + str(len(self.apis)) + C.RESET)
        return self.apis
