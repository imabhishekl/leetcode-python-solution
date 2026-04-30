import os
import requests
import sys
import traceback
import re
import html
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
        raise Exception(f"HTTP {res.status_code} Error. LeetCode rejected the request. Check your query or cookies.")
    return res.json()

def get_problem_info(p_slug):
    """Fetches category tags and the problem description."""
    query = {"query": "query q($s: String!) { question(titleSlug: $s) { topicTags { name } content } }", "variables": {"s": p_slug}}
    try:
        data = safe_request(query)
        q_data = data.get('data', {}).get('question', {})
        
        tags = [t['name'] for t in q_data.get('topicTags', [])]
        raw_content = q_data.get('content', '')
        
        # Strip HTML tags and decode HTML entities to make it plain text
        clean_content = html.unescape(re.sub(r'<[^>]+>', '', raw_content)).strip()
        
        return tags, clean_content
    except:
        return ["Uncategorized"], ""

def save_solution(p_slug, sub_id, lang):
    query = {"query": "query s($id: Int!) { submissionDetails(submissionId: $id) { code } }", "variables": {"id": int(sub_id)}}
    try:
        data = safe_request(query)
        source_code = data.get('data', {}).get('submissionDetails', {}).get('code', '')
        if not source_code: return False

        tags, description = get_problem_info(p_slug)
        category = tags[0].replace(" ", "_") if tags else "Uncategorized"
        
        os.makedirs(category, exist_ok=True)
        ext = { "python3": ".py", "python": ".py", "cpp": ".cpp", "java": ".java", "javascript": ".js" }.get(lang, ".txt")
        file_path = os.path.join(category, f"{p_slug}{ext}")
        
        # 1. Format the multi-line comment based on the programming language
        comment_formats = {
            ".py": ('"""\n', '\n"""\n'),
            ".cpp": ('/*\n', '\n*/\n'),
            ".java": ('/*\n', '\n*/\n'),
            ".js": ('/*\n', '\n*/\n')
        }
        start_c, end_c = comment_formats.get(ext, ('', '\n'))
        problem_url = f"https://leetcode.com/problems/{p_slug}/"
        
        # 2. Prepend the definition and URL to the code
        final_code = source_code
        if description:
            final_code = f"{start_c}Problem Link: {problem_url}\n\n{description}{end_c}\n{source_code}"

        with open(file_path, "w") as f:
            f.write(final_code)
            
        print(f"✅ Saved: {category}/{p_slug}")
        return True
    except Exception as e:
        print(f"❌ Error saving {p_slug}: {e}")
        return False

# --- 1. EXECUTION ---
try:
    if "selective" in sync_mode and slug:
        print(f"🔍 Selective Sync for: {slug}")
        # FIXED: Strictly typed GraphQL query variables
        query = {
            "query": "query subList($offset: Int!, $limit: Int!, $questionSlug: String!) { submissionList(offset: $offset, limit: $limit, questionSlug: $questionSlug) { submissions { id, statusDisplay, lang } } }",
            "variables": {"offset": 0, "limit": 10, "questionSlug": slug}
        }
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
            # FIXED: Strictly typed GraphQL query variables for Timeline
            query = {
                "query": "query subList($offset: Int!, $limit: Int!, $questionSlug: String!) { submissionList(offset: $offset, limit: $limit, questionSlug: $questionSlug) { submissions { id, timestamp, statusDisplay, lang, titleSlug } } }",
                "variables": {"offset": offset, "limit": 20, "questionSlug": ""}
            }
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

    # --- 2. THE VISUAL TREE GENERATOR ---
    root_readme_path = "README.md"
    print("📝 Rebuilding Visual Tree Structure...")
    
    valid_exts = ['py', 'cpp', 'java', 'js', 'txt']
    categories = []
    
    for d in os.listdir('.'):
        if os.path.isdir(d) and d not in {'.git', '.github', 'scripts'}:
            if any(f.split('.')[-1] in valid_exts for f in os.listdir(d)):
                categories.append(d)
    
    categories.sort()
    tree_md = "\n"
    
    for cat in categories:
        tree_md += f"### 📂 {cat.replace('_', ' ')}\n"
        solutions = sorted([f for f in os.listdir(cat) if f.split('.')[-1] in valid_exts])
        
        for sol in solutions:
            display_name = os.path.splitext(sol)[0]
            leetcode_url = f"https://leetcode.com/problems/{display_name}/"
            tree_md += f"  * 📄 [{display_name}](./{cat}/{sol}) | [🔗 LeetCode]({leetcode_url})\n"
        tree_md += "\n"

    start_marker = ""
    end_marker = ""

    header_text = ""
    footer_text = ""
    
    if os.path.exists(root_readme_path):
        with open(root_readme_path, "r") as f:
            full_content = f.read()
            
        start_pos = full_content.find(start_marker)
        end_pos = full_content.find(end_marker)
        
        if start_pos != -1 and end_pos != -1:
            header_text = full_content[:start_pos].strip()
            footer_text = full_content[end_pos + len(end_marker):].strip()

    if not header_text:
        header_text = """# 🧑‍💻 LeetCode Problem Solving Portfolio\n\nWelcome to my LeetCode algorithm portfolio! This repository serves as a centralized, continuous log of my problem-solving practice, data structure exploration, and technical interview preparation.\n\n## ⚙️ Repository Automation\nThis repository is automatically maintained via a custom **GitHub Actions CI/CD Pipeline**.\n\nWhenever I complete a problem, an on-demand workflow triggers a Python script that hits the LeetCode GraphQL API, fetches my accepted code, generates a minimalist problem reference, and pushes the commit directly to this repository.\n\n## 📂 Structure\nThe solutions are organized by **Category** (e.g., Array, Sliding Window, Dynamic Programming).\n* **Category Folders:** Grouping by computer science concepts.\n* **Solution Files:** Each file is named after the problem slug for quick reference.\n\n## 📝 Problems Solved"""

    if not footer_text:
        footer_text = "---\n*Generated automatically to track algorithmic problem-solving progress.*"

    final_readme = f"{header_text}\n\n{start_marker}\n{tree_md}{end_marker}\n\n{footer_text}\n"

    with open(root_readme_path, "w") as f:
        f.write(final_readme)
    print("🚀 README tree structure updated with external links!")

except Exception as e:
    print(f"\n🔥 FATAL SCRIPT CRASH: {e}")
    traceback.print_exc()
    sys.exit(1)
