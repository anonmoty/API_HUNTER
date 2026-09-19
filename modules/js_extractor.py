import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.colors import C
from core.config import Config

class JSExtractor:
    name = "JavaScript API Extractor"

    def __init__(self, url):
        self.url = url
        self.apis = []

    def run(self):
        print("\n" + C.B + "=" * 62 + C.RESET)
        print("  " + C.BOLD + C.G + "[1/12] JAVASCRIPT API EXTRACTOR" + C.RESET)
        print(C.B + "=" * 62 + C.RESET)

        js_files = []
        inline_js = ""

        try:
            resp = requests.get(self.url, timeout=Config.TIMEOUT, headers=Config.HEADERS)
            soup = BeautifulSoup(resp.text, "html.parser")
            for script in soup.find_all("script", src=True):
                src = urljoin(self.url, script["src"])
                js_files.append(src)
            for script in soup.find_all("script"):
                if script.string:
                    inline_js += script.string + "\n"
            print("  " + C.ok("JS files: " + str(len(js_files))))
        except Exception as e:
            print("  " + C.fail("Page fetch failed: " + str(e)))
            return self.apis

        self.apis.extend(self._extract(inline_js))

        def fetch_js(js_url):
            try:
                r = requests.get(js_url, timeout=Config.TIMEOUT, headers=Config.HEADERS)
                if r.status_code == 200:
                    return self._extract(r.text)
            except Exception:
                pass
            return []

        with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as ex:
            futures = {ex.submit(fetch_js, j): j for j in js_files[:50]}
            done = 0
            for future in as_completed(futures):
                done += 1
                if done % 10 == 0:
                    C.bar(done, len(futures), "Scanning JS...")
                result = future.result()
                self.apis.extend(result)

        self.apis = list(set(self.apis))
        print("\n  " + C.BOLD + C.G + "[+] APIs from JS: " + str(len(self.apis)) + C.RESET)
        for a in self.apis[:15]:
            print("    " + C.api(a))
        if len(self.apis) > 15:
            print("    " + C.D + "... and " + str(len(self.apis) - 15) + " more" + C.RESET)
        return self.apis

    def _extract(self, text):
        found = []
        for pattern in Config.JS_API_PATTERNS:
            for m in re.findall(pattern, text, re.IGNORECASE):
                m = m.strip()
                if len(m) > 3 and len(m) < 200 and not m.endswith((".js", ".css", ".png", ".jpg", ".svg")):
                    if m.startswith("/"):
                        full = self.url.rstrip("/") + m
                    elif m.startswith("http"):
                        full = m
                    else:
                        full = self.url.rstrip("/") + "/" + m
                    found.append(full)
        return found
