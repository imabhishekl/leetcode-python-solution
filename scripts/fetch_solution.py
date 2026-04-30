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

# --- 2. GET TOPIC TAGS (CATEGORIES) ---
tags_query = {
    "query": """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        topicTags { name }
      }
    }
    """,
    "variables": {"titleSlug": slug}
}
tags_data = requests.post(url, json=tags_query, headers=headers).json()
tags_list = [t['name'] for t in tags_data['data']['question']['topicTags']]

# Use the first tag as the main folder category (e.g., "Sliding Window" -> "Sliding_Window")
primary_category = tags_list[0].replace(" ", "_") if tags_list else "Uncategorized"

# --- 3. FORMAT README & SAVE FILES IN CATEGORY FOLDER ---
# The folder path is now: Category_Name/problem-slug/
folder_path = os.path.join(primary_category, slug)
os.makedirs(folder_path, exist_ok=True)

# Add all tags to the minimalist README
readme_content = f"[{slug}](https://leetcode.com/problems/{slug}/)\n\n**Categories:** {', '.join(tags_list)}\n"

ext_map = {"python3": ".py", "python": ".py", "cpp": ".cpp", "java": ".java", "javascript": ".js"}
code_path = os.path.join(folder_path, f"solution{ext_map.get(language, '.txt')}")

with open(code_path, "w") as f:
    f.write(source_code)

readme_path = os.path.join(folder_path, "README.md")
with open(readme_path, "w") as f:
    f.write(readme_content)

print(f"Successfully saved {slug} under {primary_category}!")

# --- 4. AUTO-UPDATE THE ROOT README BY CATEGORY ---
root_readme_path = "README.md"
excluded_dirs = {'.git', '.github', 'scripts'}
index_markdown = "\n"

# Find all category folders
categories = [d for d in os.listdir('.') if os.path.isdir(d) and d not in excluded_dirs and not d.startswith('.')]
categories.sort()

# Build the Markdown index
for category in categories:
    index_markdown += f"### {category.replace('_', ' ')}\n"
    
    # Find all problems inside this category
    problems = [p for p in os.listdir(category) if os.path.isdir(os.path.join(category, p))]
    problems.sort()
    
    for prob in problems:
        index_markdown += f"- [{prob}](./{category}/{prob})\n"
    index_markdown += "\n"

# Inject into the root README
try:
    with open(root_readme_path, "r") as f:
        root_content = f.read()
        
    pattern = r"().*?()"
    replacement = rf"\1{index_markdown}\2"
    updated_readme = re.sub(pattern, replacement, root_content, flags=re.DOTALL)
    
    with open(root_readme_path, "w") as f:
        f.write(updated_readme)
        
    print("Successfully updated root README.md index by category!")
except FileNotFoundError:
    print("Root README.md not found. Skipping index update.")
