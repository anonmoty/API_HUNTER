import requests
from urllib.parse import urljoin
from core.colors import C
from core.config import Config

class SwaggerFinder:
    name = "Swagger/OpenAPI Finder"

    def __init__(self, url):
        self.url = url
        self.apis = []

    def run(self):
        print("\n" + C.B + "=" * 62 + C.RESET)
        print("  " + C.BOLD + C.G + "[3/12] SWAGGER / OPENAPI FINDER" + C.RESET)
        print(C.B + "=" * 62 + C.RESET)
        print("  " + C.info("Testing " + str(len(Config.SWAGGER_PATHS)) + " paths..."))

        for path in Config.SWAGGER_PATHS:
            test_url = urljoin(self.url, path)
            try:
                resp = requests.get(test_url, timeout=Config.TIMEOUT, headers=Config.HEADERS)
                if resp.status_code == 200:
                    body = resp.text.lower()
                    if any(kw in body for kw in ["swagger", "openapi", "paths", "info"]):
                        self.apis.append(test_url)
                        print("    " + C.api("FOUND: " + test_url))
                        try:
                            data = resp.json()
                            paths = data.get("paths", {})
                            if paths:
                                print("    " + C.ok(str(len(paths)) + " endpoints in spec!"))
                                for p in paths:
                                    full = self.url.rstrip("/") + p
                                    self.apis.append(full)
                                    methods = ",".join(paths[p].keys()).upper()
                                    print("      " + C.api("[" + methods + "] " + full))
                        except Exception:
                            pass
            except Exception:
                pass

        self.apis = list(set(self.apis))
        if self.apis:
            print("\n  " + C.BOLD + C.G + "[+] Swagger APIs: " + str(len(self.apis)) + C.RESET)
        else:
            print("\n  " + C.warn("No Swagger/OpenAPI found"))
        return self.apis
