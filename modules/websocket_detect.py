import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from core.colors import C
from core.config import Config

class WebSocketDetect:
    name = "WebSocket API Detector"

    def __init__(self, url):
        self.url = url
        self.apis = []

    def run(self):
        print("\n" + C.B + "=" * 62 + C.RESET)
        print("  " + C.BOLD + C.G + "[10/12] WEBSOCKET API DETECTOR" + C.RESET)
        print(C.B + "=" * 62 + C.RESET)

        try:
            resp = requests.get(self.url, timeout=Config.TIMEOUT, headers=Config.HEADERS)
            text = resp.text

            ws_patterns = [
                r'ws://[a-zA-Z0-9.\-:]+/[a-zA-Z0-9_/\-]*',
                r'wss://[a-zA-Z0-9.\-:]+/[a-zA-Z0-9_/\-]*',
                r'new\s+WebSocket\(["\']([^"\']+)["\']',
                r'Socket\.io\(["\']([^"\']+)["\']',
                r'io\.connect\(["\']([^"\']+)["\']',
            ]

            for pattern in ws_patterns:
                matches = re.findall(pattern, text)
                for m in matches:
                    m = m.strip()
                    if m and m not in self.apis:
                        self.apis.append(m)
                        print("    " + C.api("WS: " + m))

            # Check common WS paths
            domain = urlparse(self.url).netloc
            ws_paths = ["/ws", "/websocket", "/socket.io/", "/ws/api",
                       "/api/ws", "/graphql/ws", "/subscriptions", "/cable"]
            for path in ws_paths:
                ws_url = "wss://" + domain + path
                self.apis.append(ws_url)
                print("    " + C.D + "Possible: " + ws_url + C.RESET)

        except Exception as e:
            print("  " + C.fail("Error: " + str(e)))

        self.apis = list(set(self.apis))
        print("\n  " + C.BOLD + C.G + "[+] WebSocket APIs: " + str(len(self.apis)) + C.RESET)
        return self.apis
