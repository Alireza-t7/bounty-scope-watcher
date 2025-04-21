import requests
import json

PROGRAM_SLUG = "koho"

API_URL = "https://hackerone.com/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Referer": f"https://hackerone.com/{PROGRAM_SLUG}",
    "User-Agent": "Mozilla/5.0"
}

QUERY = {
    "operationName": "TeamStructuredScopes",
    "variables": {"handle": PROGRAM_SLUG},
    "query": """
      query TeamStructuredScopes($handle: String!) {
        team(handle: $handle) {
          structured_scopes {
            edges {
              node {
                asset_identifier
                asset_type
                eligible_for_submission
                instruction
              }
            }
          }
        }
      }
    """
}

print(f"🌐 Fetching: https://hackerone.com/{PROGRAM_SLUG}")

try:
    response = requests.post(API_URL, headers=HEADERS, json=QUERY)
except Exception as e:
    print(f"❌ Request failed: {e}")
    exit()

if response.status_code != 200:
    print(f"❌ Failed to fetch data: {response.status_code}")
    with open("debug_response.json", "w") as f:
        f.write(response.text)
    exit()

data = response.json()
with open("debug_response.json", "w") as f:
    json.dump(data, f, indent=2)

# استخراج scopes
try:
    edges = data["data"]["team"]["structured_scopes"]["edges"]
    scopes = [edge["node"] for edge in edges]
except (KeyError, TypeError):
    print("❌ Could not extract scopes from response")
    exit()

if not scopes:
    print("⚠️ No scopes found.")
    exit()

# ذخیره فایل JSON
filename = f"{PROGRAM_SLUG}_scope.json"
with open(filename, "w") as f:
    json.dump(scopes, f, indent=2)

print(f"✅ Saved {len(scopes)} scopes to {filename}")