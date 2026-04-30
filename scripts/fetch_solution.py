import os
import requests
import json

# Load environment variables injected by GitHub Actions
session_cookie = os.environ.get("LEETCODE_SESSION")
csrf_token = os.environ.get("LEETCODE_CSRF_TOKEN")
slug = os.environ.get("PROBLEM_SLUG")

# LeetCode GraphQL Endpoint
url = "https://leetcode.com/graphql"

headers = {
    "Content-Type": "application/json",
    "Cookie": f"LEETCODE_SESSION={session_cookie}; csrftoken={csrf_token}",
    "x-csrftoken": csrf_token,
    "Referer": f"https://leetcode.com/problems/{slug}/"
}

# 1. Query to find your recent accepted submissions for this specific problem
submissions_query = {
    "query": """
    query submissionList($offset: Int!, $limit: Int!, $questionSlug: String!) {
      submissionList(offset: $offset, limit: $limit, questionSlug: $questionSlug) {
        submissions {
          id
          statusDisplay
          lang
        }
      }
    }
    """,
    "variables": {
        "offset": 0,
        "limit": 10,
        "questionSlug": slug
    }
}

response = requests.post(url, json=submissions_query, headers=headers)
data = response.json()

# Filter for the most recent "Accepted" submission
accepted_subs = [s for s in data['data']['submissionList']['submissions'] if s['statusDisplay'] == 'Accepted']

if not accepted_subs:
    print(f"No accepted submissions found for {slug}.")
    exit(1)

target_submission_id = accepted_subs[0]['id']
language = accepted_subs[0]['lang']

# 2. Query to get the actual code for that submission ID
code_query = {
    "query": """
    query submissionDetails($submissionId: Int!) {
      submissionDetails(submissionId: $submissionId) {
        code
      }
    }
    """,
    "variables": {
        "submissionId": int(target_submission_id)
    }
}

code_response = requests.post(url, json=code_query, headers=headers)
code_data = code_response.json()
source_code = code_data['data']['submissionDetails']['code']

# 3. Save the file locally (GitHub Action will commit this in the next step)
# Map LeetCode language names to file extensions
ext_map = {"python3": ".py", "python": ".py", "cpp": ".cpp", "java": ".java", "javascript": ".js"}
file_ext = ext_map.get(language, ".txt")
file_path = f"{slug}{file_ext}"

with open(file_path, "w") as f:
    f.write(source_code)

print(f"Successfully fetched and saved {file_path}")
