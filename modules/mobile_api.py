import requests
import re
from urllib.parse import urlparse
from core.colors import C
from core.config import Config

class MobileAPI:
    name = "Mobile App API Detector"

    def __init__(self, url):
        self.url = url
        self.apis = []

    def run(self):
        print("\n" + C.B + "=" * 62 + C.RESET)
        print("  " + C.BOLD + C.G + "[11/12] MOBILE APP API DETECTOR" + C.RESET)
        print(C.B + "=" * 62 + C.RESET)

        domain = urlparse(self.url).netloc

        # Check for mobile-specific API patterns
        mobile_paths = [
            "/api/mobile", "/api/app", "/api/ios", "/api/android",
            "/api/v1/mobile", "/api/v1/app", "/api/v1/device",
            "/api/push", "/api/fcm", "/api/notifications",
            "/api/deeplink", "/api/universal-link",
            "/.well-known/apple-app-site-association",
            "/.well-known/assetlinks.json",
            "/api/v1/auth/mobile", "/api/v1/auth/app",
        ]

        print("  " + C.info("Checking mobile API paths..."))
        for path in mobile_paths:
            test_url = self.url.rstrip("/") + path
            try:
                resp = requests.get(test_url, timeout=5, headers=Config.HEADERS, allow_redirects=False)
                if resp.status_code in [200, 401, 403, 405]:
                    self.apis.append(test_url)
                    print("    " + C.api("[" + str(resp.status_code) + "] " + test_url))
            except Exception:
                pass

        # Check for app store links (reveal API domains)
        print("  " + C.info("Checking app store links..."))
        try:
            resp = requests.get(self.url, timeout=Config.TIMEOUT, headers=Config.HEADERS)
            app_links = re.findall(r'(https?://apps\.apple\.com/[^\s"\'<>]+|https?://play\.google\.com/store/apps/[^\s"\'<>]+)', resp.text)
            for link in app_links:
                print("    " + C.info("App: " + link))

            # Check for API domains in meta tags
            api_domains = re.findall(r'content=["\'](https?://api\.[^"\']+)["\']', resp.text)
            for d in api_domains:
                self.apis.append(d)
                print("    " + C.api("Mobile API domain: " + d))
        except Exception:
            pass

        self.apis = list(set(self.apis))
        print("\n  " + C.BOLD + C.G + "[+] Mobile APIs: " + str(len(self.apis)) + C.RESET)
        return self.apis
