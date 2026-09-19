import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.colors import C
from core.config import Config

class PathBrute:
    name = "API Path Bruteforcer"

    def __init__(self, url):
        self.url = url
        self.apis = []

    def _check(self, path):
        test_url = urljoin(self.url, path)
        try:
            resp = requests.get(test_url, timeout=5, headers=Config.HEADERS, allow_redirects=False)
            if resp.status_code in [200, 301, 302, 401, 403, 405]:
                return (test_url, resp.status_code, len(resp.text))
        except Exception:
            pass
        return None

    def run(self):
        print("\n" + C.B + "=" * 62 + C.RESET)
        print("  " + C.BOLD + C.G + "[6/12] API PATH BRUTEFORCER" + C.RESET)
        print(C.B + "=" * 62 + C.RESET)
        print("  " + C.info("Paths: " + str(len(Config.API_PATHS))) + " | Threads: " + str(Config.MAX_THREADS))

        with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as ex:
            futures = {ex.submit(self._check, p): p for p in Config.API_PATHS}
            done = 0
            for future in as_completed(futures):
                done += 1
                if done % 20 == 0:
                    C.bar(done, len(futures), "Bruting...")
                result = future.result()
                if result:
                    url, status, size = result
                    self.apis.append(url)
                    color = C.G if status == 200 else C.Y if status in [401, 403] else C.CY
                    print("\n    " + color + "[" + str(status) + "]" + C.RESET + " " + url + " (" + str(size) + "B)")

        print("\n  " + C.BOLD + C.G + "[+] Paths found: " + str(len(self.apis)) + C.RESET)
        return self.apis
