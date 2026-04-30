import os
import requests
import re

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
readme_content = f"[{slug}](https://leetcode.com/problems/{slug}/)\n"

# --- 3. SAVE TO A FOLDER ---
os.makedirs(slug, exist_ok=True)

ext_map = {"python3": ".py", "python": ".py", "cpp": ".cpp", "java": ".java", "javascript": ".js"}
code_path = os.path.join(slug, f"solution{ext_map.get(language, '.txt')}")

with open(code_path, "w") as f:
    f.write(source_code)

readme_path = os.path.join(slug, "README.md")
with open(readme_path, "w") as f:
    f.write(readme_content)

print(f"Successfully saved {slug}!")

# --- 4. AUTO-UPDATE THE ROOT README.MD INDEX ---
root_readme_path = "README.md"
excluded_dirs = {'.git', '.github', 'scripts'}
problem_folders = []

# Scan the current directory for folders
for item in os.listdir('.'):
    if os.path.isdir(item) and item not in excluded_dirs and not item.startswith('.'):
        problem_folders.append(item)

# Alphabetize the list of problems
problem_folders.sort()

# Create the Markdown list with clickable links
index_list = "\n".join([f"- [{folder}](./{folder})" for folder in problem_folders])
index_list = "\n" + index_list + "\n"

# Read the root README, replace the text between the markers, and write it back
try:
    with open(root_readme_path, "r") as f:
        root_content = f.read()
        
    pattern = r"().*?()"
    replacement = rf"\1{index_list}\2"
    updated_readme = re.sub(pattern, replacement, root_content, flags=re.DOTALL)
    
    with open(root_readme_path, "w") as f:
        f.write(updated_readme)
        
    print("Successfully updated root README.md index!")
except FileNotFoundError:
    print("Root README.md not found. Skipping index update.")
