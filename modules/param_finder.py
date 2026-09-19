import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from core.colors import C
from core.config import Config

class ParamFinder:
    name = "API Parameter Finder"

    def __init__(self, url):
        self.url = url
        self.apis = []

    def run(self):
        print("\n" + C.B + "=" * 62 + C.RESET)
        print("  " + C.BOLD + C.G + "[7/12] API PARAMETER FINDER" + C.RESET)
        print(C.B + "=" * 62 + C.RESET)

        try:
            resp = requests.get(self.url, timeout=Config.TIMEOUT, headers=Config.HEADERS)
            soup = BeautifulSoup(resp.text, "html.parser")

            for a in soup.find_all("a", href=True):
                if "?" in a["href"] and "=" in a["href"]:
                    full = urljoin(self.url, a["href"])
                    self.apis.append(full)
                    print("    " + C.api(full))

            params = re.findall(r'["\']([^"\']*\?[a-zA-Z_]+=[^"\']*)["\']', resp.text)
            for p in params:
                if p.startswith("http") or p.startswith("/"):
                    full = urljoin(self.url, p)
                    self.apis.append(full)

            print("\n  " + C.info("Testing reflection..."))
            for param in ["id", "q", "search", "page", "file", "url", "path", "name", "callback", "redirect"]:
                test_url = self.url.rstrip("/") + "?" + param + "=apitest99"
                try:
                    r = requests.get(test_url, timeout=5, headers=Config.HEADERS)
                    if "apitest99" in r.text:
                        self.apis.append(test_url)
                        print("    " + C.warn("Reflected: ?" + param + "="))
                except Exception:
                    pass
        except Exception as e:
            print("  " + C.fail("Error: " + str(e)))

        self.apis = list(set(self.apis))
        print("\n  " + C.BOLD + C.G + "[+] Parameterized URLs: " + str(len(self.apis)) + C.RESET)
        return self.apis
