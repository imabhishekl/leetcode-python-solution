import os
import requests
import re
import sys
from datetime import datetime

# --- CONFIG ---
session_cookie = os.environ.get("LEETCODE_SESSION")
csrf_token = os.environ.get("LEETCODE_CSRF_TOKEN")
sync_mode = os.environ.get("SYNC_MODE", "").lower()
slug = os.environ.get("PROBLEM_SLUG")
start_date_str = os.environ.get("START_DATE", "2026-04-01")

url = "https://leetcode.com/graphql"
headers = {
    "Content-Type": "application/json",
    "Cookie": f"LEETCODE_SESSION={session_cookie}; csrftoken={csrf_token}",
    "x-csrftoken": csrf_token,
    "Referer": "https://leetcode.com"
}

def get_problem_info(p_slug):
    query = {"query": "query q($s: String!) { question(titleSlug: $s) { topicTags { name } } }", "variables": {"s": p_slug}}
    try:
        res = requests.post(url, json=query, headers=headers).json()
        return [t['name'] for t in res.get('data', {}).get('question', {}).get('topicTags', [])]
    except:
        return ["Uncategorized"]

def save_solution(p_slug, sub_id, lang):
    query = {"query": "query s($id: Int!) { submissionDetails(submissionId: $id) { code } }", "variables": {"id": int(sub_id)}}
    try:
        res = requests.post(url, json=query, headers=headers).json()
        source_code = res['data']['submissionDetails']['code']
        tags = get_problem_info(p_slug)
        category = tags[0].replace(" ", "_") if tags else "Uncategorized"
        
        os.makedirs(category, exist_ok=True)
        ext = { "python3": ".py", "python": ".py", "cpp": ".cpp", "java": ".java", "javascript": ".js" }.get(lang, ".txt")
        file_path = os.path.join(category, f"{p_slug}{ext}")
        
        with open(file_path, "w") as f:
            f.write(source_code)
        print(f"✅ Saved: {category}/{p_slug}")
        return True
    except Exception as e:
        print(f"❌ Error saving {p_slug}: {e}")
        return False

# --- 1. EXECUTION ---
success_count = 0
if "selective" in sync_mode and slug:
    query = {"query": "query subList($s: String!) { submissionList(offset: 0, limit: 10, questionSlug: $s) { submissions { id, statusDisplay, lang } } }", "variables": {"s": slug}}
    res = requests.post(url, json=query, headers=headers).json()
    subs = res.get('data', {}).get('submissionList', {}).get('submissions', [])
    accepted = [s for s in subs if s['statusDisplay'] == 'Accepted']
    if accepted and save_solution(slug, accepted[0]['id'], accepted[0]['lang']):
        success_count += 1

elif "timeline" in sync_mode:
    start_ts = datetime.strptime(start_date_str, "%Y-%m-%d").timestamp()
    offset, has_more = 0, True
    while has_more:
        query = {"query": "query subList($o: Int!, $l: Int!) { submissionList(offset: $o, limit: 20) { submissions { id, timestamp, statusDisplay, lang, titleSlug } } }", "variables": {"o": offset, "l": 20}}
        res = requests.post(url, json=query, headers=headers).json()
        subs = res.get('data', {}).get('submissionList', {}).get('submissions', [])
        if not subs: break
        for s in subs:
            if int(s['timestamp']) < start_ts:
                has_more = False
                break
            if s['statusDisplay'] == 'Accepted':
                if save_solution(s['titleSlug'], s['id'], s['lang']):
                    success_count += 1
        offset += 20

# --- 2. THE "CLEAN" INDEXER ---
root_readme_path = "README.md"
if os.path.exists(root_readme_path):
    # Only treat a folder as a "Category" if it contains actual code files
    allowed_exts = {'.py', '.cpp', '.java', '.js', '.txt'}
    categories = []
    for d in os.listdir('.'):
        if os.path.isdir(d) and d not in {'.git', '.github', 'scripts'}:
            # Check if this folder has any valid code files
            if any(any(f.endswith(ext) for ext in allowed_exts) for f in os.listdir(d)):
                categories.append(d)
    
    categories.sort()
    
    new_index = "\n"
    for cat in categories:
        new_index += f"### {cat.replace('_', ' ')}\n"
        solutions = sorted([f for f in os.listdir(cat) if any(f.endswith(ext) for ext in allowed_exts)])
        for sol in solutions:
            new_index += f"- [{sol}](./{cat}/{sol})\n"
        new_index += "\n"

    # Read and split safely
    with open(root_readme_path, "r") as f:
        full_content = f.read()

    # Split using the first marker. We only keep what is BEFORE the first tag.
    header_part = full_content.split("")[0]
    
    # Reconstruct the file: Header + Markers + New Index + Footer Marker + Final Text
    # This prevents the "infinite append" bug
    final_output = header_part + "" + new_index + ""
    
    # If there was a specific footer after the markers, we can try to grab it
    if "" in full_content:
        footer_part = full_content.split("")[-1]
        final_output += footer_part

    with open(root_readme_path, "w") as f:
        f.write(final_output)
    print("🚀 README synchronized and cleaned.")
