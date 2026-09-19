import requests
import re
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin
from core.colors import C
from core.config import Config

class HTMLExtractor:
    name = "HTML Source Extractor"

    def __init__(self, url):
        self.url = url
        self.apis = []

    def run(self):
        print("\n" + C.B + "=" * 62 + C.RESET)
        print("  " + C.BOLD + C.G + "[2/12] HTML SOURCE EXTRACTOR" + C.RESET)
        print(C.B + "=" * 62 + C.RESET)
        try:
            resp = requests.get(self.url, timeout=Config.TIMEOUT, headers=Config.HEADERS)
            soup = BeautifulSoup(resp.text, "html.parser")

            print("  " + C.info("Forms..."))
            for form in soup.find_all("form"):
                action = form.get("action", "")
                if action and action != "#":
                    full = urljoin(self.url, action)
                    self.apis.append(full)
                    print("    " + C.api("[" + form.get("method", "GET").upper() + "] " + full))

            print("  " + C.info("API links..."))
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if any(kw in href.lower() for kw in ["/api/", "/v1/", "/v2/", "/rest/", "/graphql", "/swagger"]):
                    full = urljoin(self.url, href)
                    self.apis.append(full)
                    print("    " + C.api(full))

            print("  " + C.info("Data attributes..."))
            for tag in soup.find_all(True):
                for attr in ["data-api", "data-url", "data-endpoint", "data-action", "data-href"]:
                    val = tag.get(attr, "")
                    if val and ("/api" in val or "/v" in val):
                        full = urljoin(self.url, val)
                        self.apis.append(full)
                        print("    " + C.api(full))

            print("  " + C.info("HTML comments..."))
            for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
                urls = re.findall(r'(https?://[^\s"\'<>]+|/api/[^\s"\'<>]+|/v[0-9]+/[^\s"\'<>]+)', comment)
                for u in urls:
                    full = urljoin(self.url, u)
                    self.apis.append(full)
                    print("    " + C.warn("Leak: " + full))

        except Exception as e:
            print("  " + C.fail("Error: " + str(e)))

        self.apis = list(set(self.apis))
        print("\n  " + C.BOLD + C.G + "[+] APIs from HTML: " + str(len(self.apis)) + C.RESET)
        return self.apis
