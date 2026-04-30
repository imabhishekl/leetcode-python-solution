import os
import requests

# Load environment variables
session_cookie = os.environ.get("LEETCODE_SESSION")
csrf_token = os.environ.get("LEETCODE_CSRF_TOKEN")
slug = os.environ.get("PROBLEM_SLUG")

url = "https://leetcode.com/graphql"
headers = {
    "Content-Type": "application/json",
    "Cookie": f"LEETCODE_SESSION={session_cookie}; csrftoken={csrf_token}",
    "x-csrftoken": csrf_token,
    "Referer": f"https://leetcode.com/problems/{slug}/"
}

# --- 1. GET THE SUBMISSION CODE ---
submissions_query = {
    "query": """
    query submissionList($offset: Int!, $limit: Int!, $questionSlug: String!) {
      submissionList(offset: $offset, limit: $limit, questionSlug: $questionSlug) {
        submissions { id, statusDisplay, lang }
      }
    }
    """,
    "variables": {"offset": 0, "limit": 10, "questionSlug": slug}
}

data = requests.post(url, json=submissions_query, headers=headers).json()
accepted_subs = [s for s in data['data']['submissionList']['submissions'] if s['statusDisplay'] == 'Accepted']

if not accepted_subs:
    print(f"No accepted submissions found for {slug}.")
    exit(1)

target_id = accepted_subs[0]['id']
language = accepted_subs[0]['lang']

code_query = {
    "query": """
    query submissionDetails($submissionId: Int!) {
      submissionDetails(submissionId: $submissionId) { code }
    }
    """,
    "variables": {"submissionId": int(target_id)}
}
source_code = requests.post(url, json=code_query, headers=headers).json()['data']['submissionDetails']['code']

# --- 2. FORMAT THE MINIMAL README ---
# Creates a simple markdown hyperlink using the slug
readme_content = f"[{slug}](https://leetcode.com/problems/{slug}/)\n"

# --- 3. SAVE TO A FOLDER ---
os.makedirs(slug, exist_ok=True)

# Save the code file
ext_map = {"python3": ".py", "python": ".py", "cpp": ".cpp", "java": ".java", "javascript": ".js"}
code_path = os.path.join(slug, f"solution{ext_map.get(language, '.txt')}")

with open(code_path, "w") as f:
    f.write(source_code)

# Save the README file
readme_path = os.path.join(slug, "README.md")
with open(readme_path, "w") as f:
    f.write(readme_content)

print(f"Successfully created folder '{slug}' with code and minimalist README!")
