چimport requests
import json

PROGRAM_SLUG = "koho"
API_URL = f"https://hackerone.com/graphql"

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
            asset_identifier
            asset_type
            eligible_for_submission
            instruction
          }
        }
      }
    """
}

response = requests.post(API_URL, headers=HEADERS, json=QUERY)

if response.status_code != 200:
    print("❌ Failed to fetch data from HackerOne API")
    exit()

data = response.json()

try:
    scopes = data["data"]["team"]["structured_scopes"]
except (KeyError, TypeError):
    print("❌ Could not extract scopes from response")
    exit()

print(f"✅ Found {len(scopes)} scopes for {PROGRAM_SLUG}")

with open(f"{PROGRAM_SLUG}_scope.json", "w") as f:
    json.dump(scopes, f, indent=2)