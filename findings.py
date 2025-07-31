import os
import json
import requests
from datetime import datetime
from dateutil import parser as date_parser

# Token from environment (must be SEMGREP_API_TOKEN, not APP token)
api_token = os.getenv("SEMGREP_APP_TOKEN")
if not api_token:
    print("❌ SEMGREP_APP_TOKEN is NOT set in the environment.")
    exit(1)

headers = {
    "Authorization": f"Bearer {api_token}",
    "Accept": "application/json"
}

# Start date filter
START_DATE = date_parser.parse("2024-01-01T00:00:00Z")

# Semgrep Findings API
BASE_URL = "https://semgrep.dev/api/v1/deployments/abashir236/findings"
OUTPUT_FILE = "semgrep_findings.json"

def fetch_all_findings():
    findings = []
    url = BASE_URL
    page_count = 0

    while url:
        page_count += 1
        print(f"🔄 Fetching page {page_count}: {url}")
        resp = requests.get(url, headers=headers)

        if resp.status_code != 200:
            print(f"❌ Error: {resp.status_code} - {resp.text}")
            break

        data = resp.json()
        results = data.get("findings", [])
        print(f"  ➕ {len(results)} findings")

        for finding in results:
            found_at_str = finding.get("found_at")
            if found_at_str:
                found_at = date_parser.parse(found_at_str)
                if found_at < START_DATE:
                    print("⏹️ Stopping: reached findings older than Jan 1, 2024.")
                    return findings
            findings.append(finding)

        url = data.get("next")

    return findings

def save_findings(findings):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(findings, f, indent=2)
    print(f"\n✅ Saved {len(findings)} findings to {OUTPUT_FILE}")

if __name__ == "__main__":
    print("🔐 SEMGREP_API_TOKEN detected, starting export...")
    findings = fetch_all_findings()
    save_findings(findings)
