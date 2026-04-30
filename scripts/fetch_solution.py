import os
import requests
import re
from datetime import datetime

# Load variables
session_cookie = os.environ.get("LEETCODE_SESSION")
csrf_token = os.environ.get("LEETCODE_CSRF_TOKEN")
sync_mode = os.environ.get("SYNC_MODE") 
slug = os.environ.get("PROBLEM_SLUG")
start_date_str = os.environ.get("START_DATE")

url = "https://leetcode.com/graphql"
headers = {
    "Content-Type": "application/json",
    "Cookie": f"LEETCODE_SESSION={session_cookie}; csrftoken={csrf_token}",
    "x-csrftoken": csrf_token
}

def get_problem_info(p_slug):
    query = {
        "query": "query q($s: String!) { question(titleSlug: $s) { topicTags { name } } }",
        "variables": {"s": p_slug}
    }
    try:
        res = requests.post(url, json=query, headers=headers).json()
        tags = [t['name'] for t in res['data']['question']['topicTags']]
        return tags
    except:
        return ["Uncategorized"]

def save_solution(p_slug, sub_id, lang):
    # Fetch code
    query = {
        "query": "query s($id: Int!) { submissionDetails(submissionId: $id) { code } }",
        "variables": {"id": int(sub_id)}
    }
    code = requests.post(url, json=query, headers=headers).json()['data']['submissionDetails']['code']
    
    # Get Category and clean it for folder names
    tags = get_problem_info(p_slug)
    category = tags[0].replace(" ", "_") if tags else "Uncategorized"
    
    # Create category folder
    os.makedirs(category, exist_ok=True)
    
    # Extension mapping
    ext = { "python3": ".py", "python": ".py", "cpp": ".cpp", "java": ".java", "javascript": ".js" }.get(lang, ".txt")
    
    # SAVE FILE: Category/problem-slug.py
    file_path = os.path.join(category, f"{p_slug}{ext}")
    with open(file_path, "w") as f:
        f.write(code)
    print(f"✅ Synced: {category}/{p_slug}{ext}")

# --- MAIN LOGIC ---
if sync_mode == "Selective (Single Problem)":
    # Get recent accepted for this slug
    query = {
        "query": "query subList($s: String!) { submissionList(offset: 0, limit: 5, questionSlug: $s) { submissions { id, statusDisplay, lang } } }",
        "variables": {"s": slug}
    }
    subs = requests.post(url, json=query, headers=headers).json()['data']['submissionList']['submissions']
    accepted = [s for s in subs if s['statusDisplay'] == 'Accepted']
    if accepted:
        save_solution(slug, accepted[0]['id'], accepted[0]['lang'])

elif sync_mode == "Timeline (All since specific date)":
    start_ts = datetime.strptime(start_date_str, "%Y-%m-%d").timestamp()
    offset, has_more = 0, True
    while has_more:
        query = {
            "query": "query subList($o: Int!, $l: Int!) { submissionList(offset: $o, limit: $l) { submissions { id, timestamp, statusDisplay, lang, titleSlug } } }",
            "variables": {"o": offset, "l": 20}
        }
        subs = requests.post(url, json=query, headers=headers).json()['data']['submissionList']['submissions']
        if not subs: break
        for s in subs:
            if int(s['timestamp']) < start_ts:
                has_more = False
                break
            if s['statusDisplay'] == 'Accepted':
                save_solution(s['titleSlug'], s['id'], s['lang'])
        offset += 20

# --- AUTO-UPDATE ROOT README INDEX ---
root_readme_path = "README.md"
excluded_dirs = {'.git', '.github', 'scripts'}
index_markdown = "\n"

# Scan for category folders
categories = sorted([d for d in os.listdir('.') if os.path.isdir(d) and d not in excluded_dirs and not d.startswith('.')])

for cat in categories:
    index_markdown += f"### {cat.replace('_', ' ')}\n"
    # Find files in this category
    solutions = sorted([f for f in os.listdir(cat) if os.path.isfile(os.path.join(cat, f))])
    for sol in solutions:
        # Link directly to the file
        index_markdown += f"- [{sol}](./{cat}/{sol})\n"
    index_markdown += "\n"

# Update README
try:
    with open(root_readme_path, "r") as f:
        content = f.read()
    pattern = r"().*?()"
    updated = re.sub(pattern, rf"\1{index_markdown}\2", content, flags=re.DOTALL)
    with open(root_readme_path, "w") as f:
        f.write(updated)
    print("🚀 Index updated successfully!")
except Exception as e:
    print(f"Error updating README: {e}")
