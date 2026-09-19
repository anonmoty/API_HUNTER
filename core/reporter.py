import json
import os
from datetime import datetime
from core.config import Config
from core.colors import C

class Reporter:
    def __init__(self, target):
        self.target = target
        self.data = {}
        self.all_apis = []
        self.start = datetime.now()
        os.makedirs(Config.OUT, exist_ok=True)

    def add(self, module, result):
        self.data[module] = result

    def add_apis(self, apis, source):
        for api in apis:
            if isinstance(api, str):
                entry = {"url": api, "source": source}
            elif isinstance(api, dict) and "url" in api:
                entry = api
                entry["source"] = source
            else:
                continue
            if entry not in self.all_apis:
                self.all_apis.append(entry)

    def get_unique_urls(self):
        seen = set()
        unique = []
        for api in self.all_apis:
            url = api.get("url", "") if isinstance(api, dict) else str(api)
            if url and url not in seen:
                seen.add(url)
                unique.append(url)
        return unique

    def save(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe = self.target.replace("://", "_").replace("/", "_").replace(":", "_").replace("?", "_")
        urls = self.get_unique_urls()

        # JSON
        jpath = os.path.join(Config.OUT, "apihunter_" + safe + "_" + ts + ".json")
        report = {
            "tool": Config.NAME, "version": Config.VERSION,
            "target": self.target, "total_unique_apis": len(urls),
            "start": self.start.strftime("%Y-%m-%d %H:%M:%S"),
            "end": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "apis": self.all_apis, "modules": self.data
        }
        with open(jpath, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print("\n  " + C.ok("JSON: " + jpath))

        # TXT with sources
        tpath = os.path.join(Config.OUT, "apihunter_" + safe + "_" + ts + ".txt")
        with open(tpath, "w") as f:
            f.write("# APIHunter v" + Config.VERSION + " Report\n")
            f.write("# Target: " + self.target + "\n")
            f.write("# Total Unique APIs: " + str(len(urls)) + "\n")
            f.write("# Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
            for api in self.all_apis:
                url = api.get("url", "") if isinstance(api, dict) else str(api)
                src = api.get("source", "") if isinstance(api, dict) else ""
                f.write(url + "  [" + src + "]\n")
        print("  " + C.ok("TXT: " + tpath))

        # URLs only (pipe-ready for nuclei, sqlmap, ffuf, etc.)
        upath = os.path.join(Config.OUT, "apihunter_" + safe + "_urls.txt")
        with open(upath, "w") as f:
            for url in urls:
                f.write(url + "\n")
        print("  " + C.ok("URLs (pipe-ready): " + upath))
        print("  " + C.info("Usage: cat " + upath + " | nuclei -t cves/"))

    def summary(self):
        urls = self.get_unique_urls()
        print("\n" + C.G + C.BOLD + "=" * 62 + C.RESET)
        print("  " + C.BOLD + "APIHUNTER v2.0 — SCAN SUMMARY" + C.RESET)
        print(C.G + "=" * 62 + C.RESET)
        print("  " + C.info("Target: " + self.target))
        dur = str(round((datetime.now() - self.start).total_seconds(), 2))
        print("  " + C.info("Duration: " + dur + "s"))
        print("  " + C.info("Total Unique APIs: " + str(len(urls))))

        sources = {}
        for api in self.all_apis:
            s = api.get("source", "Unknown") if isinstance(api, dict) else "Unknown"
            sources[s] = sources.get(s, 0) + 1

        print("\n  " + C.CY + "Breakdown by Source:" + C.RESET)
        for s, count in sorted(sources.items(), key=lambda x: -x[1]):
            print("    " + C.G + s.ljust(30) + str(count) + C.RESET)

        print("\n  " + C.CY + "Next Steps (Pipe to other tools):" + C.RESET)
        print("    " + C.D + "nuclei -l output/apihunter_*_urls.txt -t cves/" + C.RESET)
        print("    " + C.D + "sqlmap -m output/apihunter_*_urls.txt --batch" + C.RESET)
        print("    " + C.D + "ffuf -w output/apihunter_*_urls.txt -u FUZZ" + C.RESET)
        print(C.G + "=" * 62 + C.RESET)
