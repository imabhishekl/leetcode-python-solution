import os
import requests
import re
from datetime import datetime

# --- CONFIGURATION & ENV LOAD ---
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
    """Fetches category tags for a specific problem."""
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
    """Fetches code and saves it into Category/problem-slug.ext."""
    # 1. Fetch the source code
    query = {
        "query": "query s($id: Int!) { submissionDetails(submissionId: $id) { code } }",
        "variables": {"id": int(sub_id)}
    }
    try:
        code_res = requests.post(url, json=query, headers=headers).json()
        source_code = code_res['data']['submissionDetails']['code']
        
        # 2. Identify Category
        tags = get_problem_info(p_slug)
        category = tags[0].replace(" ", "_") if tags else "Uncategorized"
        
        # 3. Create folder and save file
        os.makedirs(category, exist_ok=True)
        ext = { "python3": ".py", "python": ".py", "cpp": ".cpp", "java": ".java", "javascript": ".js" }.get(lang, ".txt")
        
        file_path = os.path.join(category, f"{p_slug}{ext}")
        with open(file_path, "w") as f:
            f.write(source_code)
        print(f"✅ Successfully saved: {category}/{p_slug}{ext}")
    except Exception as e:
        print(f"❌ Error saving {p_slug}: {e}")

# --- MAIN EXECUTION LOGIC ---
if sync_mode == "Selective (Single Problem)":
    print(f"Running Selective Sync for: {slug}")
    query = {
        "query": "query subList($s: String!) { submissionList(offset: 0, limit: 5, questionSlug: $s) { submissions { id, statusDisplay, lang } } }",
        "variables": {"s": slug}
    }
    data = requests.post(url, json=query, headers=headers).json()
    subs = data['data']['submissionList']['submissions']
    accepted = [s for s in subs if s['statusDisplay'] == 'Accepted']
    if accepted:
        save_solution(slug, accepted[0]['id'], accepted[0]['lang'])
    else:
        print(f"No accepted submissions found for {slug}.")

elif sync_mode == "Timeline (All since specific date)":
    print(f"Running Timeline Sync since: {start_date_str}")
    start_ts = datetime.strptime(start_date_str, "%Y-%m-%d").timestamp()
    offset, has_more = 0, True
    
    while has_more:
        query = {
            "query": "query subList($o: Int!, $l: Int!) { submissionList(offset: $o, limit: $l) { submissions { id, timestamp, statusDisplay, lang, titleSlug } } }",
            "variables": {"o": offset, "l": 20}
        }
        res = requests.post(url, json=query, headers=headers).json()
        subs = res['data']['submissionList']['submissions']
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
    solutions = sorted([f for f in os.listdir(cat) if os.path.isfile(os.path.join(cat, f))])
    for sol in solutions:
        index_markdown += f"- [{sol}](./{cat}/{sol})\n"
    index_markdown += "\n"

# Update README with Split Logic (prevents total file reset)
try:
    if os.path.exists(root_readme_path):
        with open(root_readme_path, "r") as f:
            content = f.read()
        
        if "" in content and "" in content:
            # Split the file around the markers
            parts = re.split(r"(|)", content, flags=re.DOTALL)
            # parts list: [0:before, 1:START, 2:middle, 3:END, 4:after]
            if len(parts) >= 5:
                new_content = parts[0] + parts[1] + index_markdown + parts[3] + parts[4]
                with open(root_readme_path, "w") as f:
                    f.write(new_content)
                print("🚀 Root README index updated successfully!")
            else:
                print("⚠️ Unexpected README structure. Check markers.")
        else:
            print("❌ Markers / not found.")
    else:
        print("❌ README.md file does not exist.")
except Exception as e:
    print(f"Error updating README: {e}")
