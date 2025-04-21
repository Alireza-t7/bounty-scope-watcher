import cloudscraper
import json
import os
from bs4 import BeautifulSoup

PROGRAM_SLUG = "koho"
PROGRAM_URL = f"https://hackerone.com/{PROGRAM_SLUG}"
JSON_FILE = f"{PROGRAM_SLUG}_scope.json"

scraper = cloudscraper.create_scraper(browser={"browser": "chrome", "platform": "windows", "mobile": False})
print(f"🌐 Fetching: {PROGRAM_URL}")
response = scraper.get(PROGRAM_URL)

if response.status_code != 200:
    print(f"❌ Failed to load page: {response.status_code}")
    exit()

with open("debug.html", "w", encoding="utf-8") as f:
    f.write(response.text)

soup = BeautifulSoup(response.text, "html.parser")
data_tag = soup.find("script", {"id": "__NEXT_DATA__"})

if not data_tag:
    print("❌ Couldn't find JSON data in page.")
    exit()

raw_json = data_tag.string
parsed_json = json.loads(raw_json)

try:
    assets = parsed_json["props"]["pageProps"]["hacktivityProgram"]["structured_scopes"]
except KeyError:
    print("❌ Scope data not found in JSON.")
    exit()

scopes = []
for asset in assets:
    scopes.append({
        "type": asset.get("asset_type", "").strip(),
        "identifier": asset.get("asset_identifier", "").strip(),
        "instructions": asset.get("asset_instructions", "").strip()
    })

print(f"✅ Found {len(scopes)} scopes.")

if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w") as f:
        json.dump(scopes, f, indent=2)
    print(f"📦 First version saved to {JSON_FILE}")
else:
    with open(JSON_FILE, "r") as f:
        old_scopes = json.load(f)

    if scopes != old_scopes:
        with open(JSON_FILE, "w") as f:
            json.dump(scopes, f, indent=2)
        print(f"🆕 Changes detected. JSON updated.")
    else:
        print("🔁 No changes detected.")
