import os
import requests
import sys
import traceback
from datetime import datetime

# --- CONFIG ---
session_cookie = os.environ.get("LEETCODE_SESSION", "")
csrf_token = os.environ.get("LEETCODE_CSRF_TOKEN", "")
sync_mode = os.environ.get("SYNC_MODE", "").lower()
slug = os.environ.get("PROBLEM_SLUG", "")
start_date_str = os.environ.get("START_DATE", "2026-04-01")

url = "https://leetcode.com/graphql"
headers = {
    "Content-Type": "application/json",
    "Cookie": f"LEETCODE_SESSION={session_cookie}; csrftoken={csrf_token}",
    "x-csrftoken": csrf_token,
    "Referer": "https://leetcode.com"
}

def safe_request(query):
    res = requests.post(url, json=query, headers=headers)
    if res.status_code != 200:
        raise Exception(f"HTTP {res.status_code} Error. Check if your LeetCode Cookies are expired.")
    return res.json()

def get_problem_info(p_slug):
    query = {"query": "query q($s: String!) { question(titleSlug: $s) { topicTags { name } } }", "variables": {"s": p_slug}}
    try:
        data = safe_request(query)
        return [t['name'] for t in data.get('data', {}).get('question', {}).get('topicTags', [])]
    except:
        return ["Uncategorized"]

def save_solution(p_slug, sub_id, lang):
    query = {"query": "query s($id: Int!) { submissionDetails(submissionId: $id) { code } }", "variables": {"id": int(sub_id)}}
    try:
        data = safe_request(query)
        source_code = data.get('data', {}).get('submissionDetails', {}).get('code', '')
        if not source_code: return False

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
try:
    if "selective" in sync_mode and slug:
        print(f"🔍 Selective Sync for: {slug}")
        query = {"query": "query subList($s: String!) { submissionList(offset: 0, limit: 10, questionSlug: $s) { submissions { id, statusDisplay, lang } } }", "variables": {"s": slug}}
        data = safe_request(query)
        subs = data.get('data', {}).get('submissionList', {}).get('submissions', [])
        accepted = [s for s in subs if s.get('statusDisplay') == 'Accepted']
        if accepted:
            save_solution(slug, accepted[0]['id'], accepted[0]['lang'])

    elif "timeline" in sync_mode:
        print(f"⏳ Timeline Sync since: {start_date_str}")
        start_ts = datetime.strptime(start_date_str, "%Y-%m-%d").timestamp()
        offset, has_more = 0, True
        while has_more:
            query = {"query": "query subList($o: Int!, $l: Int!) { submissionList(offset: $o, limit: 20) { submissions { id, timestamp, statusDisplay, lang, titleSlug } } }", "variables": {"o": offset, "l": 20}}
            data = safe_request(query)
            subs = data.get('data', {}).get('submissionList', {}).get('submissions', [])
            if not subs: break
            for s in subs:
                if int(s.get('timestamp', 0)) < start_ts:
                    has_more = False
                    break
                if s.get('statusDisplay') == 'Accepted':
                    save_solution(s.get('titleSlug'), s.get('id'), s.get('lang'))
            offset += 20

    # --- 2. THE SELF-HEALING TREE GENERATOR ---
    root_readme_path = "README.md"
    print("📝 Rebuilding Tree Structure...")
    
    allowed_exts = {'.py', '.cpp', '.java', '.js', '.txt'}
    categories = []
    
    # 1. Gather all actual categories and code files
    for d in os.listdir('.'):
        if os.path.isdir(d) and d not in {'.git', '.github', 'scripts'}:
            if any(any(f.endswith(ext) for ext in allowed_exts) for f in os.listdir(d)):
                categories.append(d)
    
    categories.sort()
    tree_md = "\n"
    for cat in categories:
        tree_md += f"### {cat.replace('_', ' ')}\n"
        solutions = sorted([f for f in os.listdir(cat) if any(f.endswith(ext) for ext in allowed_exts)])
        for sol in solutions:
            # Strip the file extension for a cleaner display name!
            display_name = os.path.splitext(sol)[0]
            tree_md += f"- [{display_name}](./{cat}/{sol})\n"
        tree_md += "\n"

    # 2. Setup safe markers
    start_marker = ""
    end_marker = ""

    # 3. Read current file to see if we can save custom changes
    header_text = ""
    footer_text = ""
    
    if os.path.exists(root_readme_path):
        with open(root_readme_path, "r") as f:
            full_content = f.read()
            
        start_pos = full_content.find(start_marker)
        end_pos = full_content.find(end_marker)
        
        if start_pos != -1 and end_pos != -1:
            # Markers exist! Keep the exact header and footer.
            header_text = full_content[:start_pos].strip()
            footer_text = full_content[end_pos + len(end_marker):].strip()

    # 4. If markers are missing (like right now), inject the default master template!
    if not header_text:
        header_text = """# 🧑‍💻 LeetCode Problem Solving Portfolio

Welcome to my LeetCode algorithm portfolio! This repository serves as a centralized, continuous log of my problem-solving practice, data structure exploration, and technical interview preparation.

## ⚙️ Repository Automation
This repository is automatically maintained via a custom **GitHub Actions CI/CD Pipeline**. 

Whenever I complete a problem, an on-demand workflow triggers a Python script that hits the LeetCode GraphQL API, fetches my accepted code, generates a minimalist problem reference, and pushes the commit directly to this repository.

## 📂 Structure
The solutions are organized by **Category** (e.g., Array, Sliding Window, Dynamic Programming).
* **Category Folders:** Grouping by computer science concepts.
* **Solution Files:** Each file is named after the problem slug for quick reference.

## 📝 Problems Solved"""

    if not footer_text:
        footer_text = "---\n*Generated automatically to track algorithmic problem-solving progress.*"

    # 5. Assemble and write the final indestructible README
    final_readme = f"{header_text}\n\n{start_marker}\n{tree_md}{end_marker}\n\n{footer_text}\n"

    with open(root_readme_path, "w") as f:
        f.write(final_readme)
    print("🚀 README successfully protected and updated!")

except Exception as e:
    print(f"\n🔥 FATAL SCRIPT CRASH: {e}")
    traceback.print_exc()
    sys.exit(1)
