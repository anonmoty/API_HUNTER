import requests
from urllib.parse import urlparse
from core.colors import C
from core.config import Config

class WaybackAPI:
    name = "Wayback Machine APIs"

    def __init__(self, url):
        self.url = url
        self.apis = []

    def run(self):
        print("\n" + C.B + "=" * 62 + C.RESET)
        print("  " + C.BOLD + C.G + "[5/12] WAYBACK MACHINE API FINDER" + C.RESET)
        print(C.B + "=" * 62 + C.RESET)

        domain = urlparse(self.url).netloc
        print("  " + C.info("Searching: " + domain))

        sources = [
            ("Wayback", "https://web.archive.org/cdx/search/cdx?url=" + domain + "/*&output=text&fl=original&collapse=urlkey&limit=1000"),
            ("CommonCrawl", "https://index.commoncrawl.org/CC-MAIN-2024-10-index?url=" + domain + "/*&output=text&fl=url&limit=500"),
        ]

        api_kw = ["/api/", "/v1/", "/v2/", "/v3/", "/rest/", "/graphql",
                  "/swagger", "/docs", "/health", "/actuator", "/metrics",
                  "/auth", "/login", "/users", "/admin", "/config",
                  "/webhook", "/callback", "/upload", "/download"]

        for name, api_url in sources:
            try:
                resp = requests.get(api_url, timeout=20, headers=Config.HEADERS)
                if resp.status_code == 200:
                    urls = resp.text.strip().split("\n")
                    for u in urls:
                        u = u.strip()
                        if any(kw in u.lower() for kw in api_kw):
                            self.apis.append(u)
                    print("  " + C.ok(name + ": " + str(len(urls)) + " URLs checked"))
            except Exception:
                print("  " + C.warn(name + " unavailable"))

        self.apis = list(set(self.apis))
        print("\n  " + C.BOLD + C.G + "[+] Wayback APIs: " + str(len(self.apis)) + C.RESET)
        for a in self.apis[:15]:
            print("    " + C.api(a))
        if len(self.apis) > 15:
            print("    " + C.D + "... and " + str(len(self.apis) - 15) + " more" + C.RESET)
        return self.apis
