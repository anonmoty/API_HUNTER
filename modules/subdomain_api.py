import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.colors import C
from core.config import Config

class SubdomainAPI:
    name = "Subdomain API Discovery"

    def __init__(self, url):
        self.url = url
        self.apis = []

    def _check_sub(self, sub, domain):
        target = "https://" + sub + "." + domain
        try:
            resp = requests.get(target, timeout=5, headers=Config.HEADERS, allow_redirects=False)
            if resp.status_code in [200, 301, 302, 401, 403]:
                return (target, resp.status_code)
        except Exception:
            pass
        return None

    def run(self):
        print("\n" + C.B + "=" * 62 + C.RESET)
        print("  " + C.BOLD + C.G + "[8/12] SUBDOMAIN API DISCOVERY" + C.RESET)
        print(C.B + "=" * 62 + C.RESET)

        domain = urlparse(self.url).netloc
        print("  " + C.info("Domain: " + domain))

        with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as ex:
            futures = {ex.submit(self._check_sub, s, domain): s for s in Config.API_SUBDOMAINS}
            done = 0
            for future in as_completed(futures):
                done += 1
                if done % 10 == 0:
                    C.bar(done, len(futures), "Checking...")
                result = future.result()
                if result:
                    target, status = result
                    self.apis.append(target)
                    print("\n    " + C.api("[" + str(status) + "] " + target))

        try:
            resp = requests.get("https://crt.sh/?q=%25." + domain + "&output=json", timeout=15)
            if resp.status_code == 200:
                for entry in resp.json():
                    name = entry.get("name_value", "").strip().lower()
                    if any(kw in name for kw in ["api", "graphql", "rest", "auth", "gateway"]):
                        target = "https://" + name
                        if target not in self.apis:
                            self.apis.append(target)
                            print("    " + C.api("CT: " + target))
        except Exception:
            pass

        self.apis = list(set(self.apis))
        print("\n  " + C.BOLD + C.G + "[+] API subdomains: " + str(len(self.apis)) + C.RESET)
        return self.apis
