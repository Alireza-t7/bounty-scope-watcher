import cloudscraper
import json
from bs4 import BeautifulSoup

PROGRAM_SLUG = "koho"
URL = f"https://hackerone.com/{PROGRAM_SLUG}"
FILENAME = f"{PROGRAM_SLUG}_scope.json"

scraper = cloudscraper.create_scraper()
res = scraper.get(URL)

if res.status_code != 200:
    print("❌ Failed to load page")
    exit()

soup = BeautifulSoup(res.text, "html.parser")
script_tag = soup.find("script", {"id": "__NEXT_DATA__"})

if not script_tag:
    print("❌ Couldn't find JSON in page")
    exit()

data = json.loads(script_tag.string)
try:
    scopes = data["props"]["pageProps"]["hacktivityProgram"]["structured_scopes"]
except KeyError:
    print("❌ No structured_scopes found")
    exit()

print(f"✅ Found {len(scopes)} scopes")
with open(FILENAME, "w") as f:
    json.dump(scopes, f, indent=2)