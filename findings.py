import os

# Read the token from environment
api_token = os.getenv("SEMGREP_API_TOKEN")

# Check if the token exists and print debug info
if api_token:
    print("✅ SEMGREP_API_TOKEN is present in environment.")
    print(f"Length: {len(api_token)} characters")
    print(f"Starts with: {api_token[:5]}... (rest hidden)")
else:
    print("❌ SEMGREP_API_TOKEN is NOT set in the environment.")
