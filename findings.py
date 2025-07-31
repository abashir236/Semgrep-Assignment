#
import os
import requests
import json
from datetime import datetime
from dateutil import parser as date_parser

API_TOKEN = os.getenv("SEMGREP_API_TOKEN")
API_URL = "https://semgrep.dev/api/v1/findings"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
}

START_DATE = date_parser.parse("2024-01-01T00:00:00Z")
LIMIT_PER_PAGE = 1000
OUTPUT_FILE = "semgrep_findings.json"

def fetch_findings():
    all_findings = []
    page = 1

    while True:
        params = {
            "limit": LIMIT_PER_PAGE,
            "page": page,
            "sort": "desc",
            "sort_by": "found_at"
        }

        print(f"Fetching page {page}...")
        response = requests.get(API_URL, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        data = response.json()
        findings = data.get("results", [])
        if not findings:
            break

        for finding in findings:
            found_at = date_parser.parse(finding.get("found_at", "1970-01-01"))
            if found_at < START_DATE:
                print("Stopping: older than Jan 1, 2024.")
                return all_findings
            all_findings.append(finding)

        if not data.get("next"):
            break
        page += 1

    return all_findings

def save_to_file(findings):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(findings, f, indent=2)
    print(f"✅ Saved {len(findings)} findings to {OUTPUT_FILE}")

if __name__ == "__main__":
    findings = fetch_findings()
    save_to_file(findings)
