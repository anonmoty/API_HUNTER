import requests
import re
from urllib.parse import urljoin
from core.colors import C
from core.config import Config

class SitemapRobots:
    name = "Sitemap & Robots.txt Parser"

    def __init__(self, url):
        self.url = url
        self.apis = []

    def run(self):
        print("\n" + C.B + "=" * 62 + C.RESET)
        print("  " + C.BOLD + C.G + "[9/12] SITEMAP & ROBOTS.TXT PARSER" + C.RESET)
        print(C.B + "=" * 62 + C.RESET)

        # Robots.txt
        print("  " + C.info("Fetching robots.txt..."))
        try:
            resp = requests.get(urljoin(self.url, "/robots.txt"), timeout=Config.TIMEOUT, headers=Config.HEADERS)
            if resp.status_code == 200:
                for line in resp.text.split("\n"):
                    line = line.strip()
                    if line.lower().startswith("disallow:") or line.lower().startswith("allow:"):
                        path = line.split(":", 1)[1].strip()
                        if path and path != "/":
                            full = urljoin(self.url, path)
                            self.apis.append(full)
                            print("    " + C.api(full))
                    elif line.lower().startswith("sitemap:"):
                        sm_url = line.split(":", 1)[1].strip()
                        print("    " + C.info("Sitemap: " + sm_url))
                        self._parse_sitemap(sm_url)
        except Exception:
            print("  " + C.warn("robots.txt not found"))

        # Direct sitemap
        print("  " + C.info("Checking sitemaps..."))
        for sm in ["/sitemap.xml", "/sitemap_index.xml", "/sitemap1.xml", "/post-sitemap.xml", "/page-sitemap.xml"]:
            self._parse_sitemap(urljoin(self.url, sm))

        self.apis = list(set(self.apis))
        print("\n  " + C.BOLD + C.G + "[+] APIs from Sitemap/Robots: " + str(len(self.apis)) + C.RESET)
        return self.apis

    def _parse_sitemap(self, url):
        try:
            resp = requests.get(url, timeout=Config.TIMEOUT, headers=Config.HEADERS)
            if resp.status_code == 200 and "<url>" in resp.text.lower():
                urls = re.findall(r'<loc>(.*?)</loc>', resp.text, re.IGNORECASE)
                api_kw = ["/api/", "/v1/", "/v2/", "/rest/", "/graphql"]
                for u in urls:
                    if any(kw in u.lower() for kw in api_kw):
                        self.apis.append(u)
                        print("    " + C.api("Sitemap: " + u))
        except Exception:
            pass
