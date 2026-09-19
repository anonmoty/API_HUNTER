import requests
from urllib.parse import urljoin
from core.colors import C
from core.config import Config

class GraphQLDetect:
    name = "GraphQL Detector"

    def __init__(self, url):
        self.url = url
        self.apis = []

    def run(self):
        print("\n" + C.B + "=" * 62 + C.RESET)
        print("  " + C.BOLD + C.G + "[4/12] GRAPHQL ENDPOINT DETECTOR" + C.RESET)
        print(C.B + "=" * 62 + C.RESET)

        for path in Config.GRAPHQL_PATHS:
            test_url = urljoin(self.url, path)
            try:
                h = dict(Config.HEADERS)
                h["Content-Type"] = "application/json"
                resp = requests.post(test_url, json={"query": "{__typename}"}, headers=h, timeout=Config.TIMEOUT)
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        if "data" in data:
                            self.apis.append(test_url)
                            print("    " + C.api("GRAPHQL: " + test_url))
                            r2 = requests.post(test_url, json={"query": "{__schema{queryType{name}}}"}, headers=h, timeout=Config.TIMEOUT)
                            if "data" in r2.text and "__schema" in r2.text:
                                print("      " + C.vuln("Introspection ENABLED!"))
                    except Exception:
                        pass
            except Exception:
                pass

        if self.apis:
            print("\n  " + C.BOLD + C.G + "[+] GraphQL: " + str(len(self.apis)) + C.RESET)
        else:
            print("\n  " + C.warn("No GraphQL found"))
        return self.apis
