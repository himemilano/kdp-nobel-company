import os
import sys
import glob
import re
import requests

WORKSPACE_DIR = "kdp_novels/workspace"
SEO_FILE = os.path.join(WORKSPACE_DIR, "04_kdp_seo_meta.md")

def find_latest_chapter():
    """📁 現在フォルダ内にある最新の章番号を特定する"""
    search_pattern = os.path.join(WORKSPACE_DIR, "03_novel_manuscript_chapter_*.md")
    files = glob.glob(search_pattern)
    
    max_chapter = 0
    for file in files:
        match = re.search(r'chapter_(\d+)\.md', file)
        if match:
            max_chapter = max(max_chapter, int(match.group(1)))
    return max_chapter

def run_compliance_check():
    print("🛡️ [KDP Legal & Compliance Dept] Executing strict copyright and Amazon KDP policy audit...")
    
    # 🔢 最新の章番号を取得
    latest_chapter = find_latest_chapter()
    
    # レポートの保存名を章ごとに動的変更
    if latest_chapter > 0:
        REPORT_FILE = os.path.join(WORKSPACE_DIR, f"05_legal_compliance_report_chapter_{latest_chapter}.md")
        manuscript_path = os.path.join(WORKSPACE_DIR, f"03_novel_manuscript_chapter_{latest_chapter}.md")
    else:
        # フォールバック（古い形式のファイルが存在する場合）
        REPORT_FILE = os.path.join(WORKSPACE_DIR, "05_legal_compliance_report.md")
        manuscript_path = os.path.join(WORKSPACE_DIR, "03_novel_manuscript.md")

    # 🛡️ 【API節約ガード】この最新章の監査レポートがすでにあるなら、APIを叩かずに即終了！
    if os.path.exists(REPORT_FILE):
        print(f"🛡️ [資産保護] 最新のChapter {latest_chapter} はすでに監査済みです（{REPORT_FILE}）。即時退勤します（API課金 ¥0）。")
        return

    # 🔗 【バトンチェック】監査対象のファイルが物理的に存在するか確認
    context = ""
    if os.path.exists(manuscript_path):
        with open(manuscript_path, "r", encoding="utf-8") as f:
            context += f"--- MANUSCRIPT (Chapter {latest_chapter}) ---\n{f.read()}\n"
    
    # SEOデータは最初の1回、または最新章とセットで確認
    if os.path.exists(SEO_FILE):
        with open(SEO_FILE, "r", encoding="utf-8") as f:
            context += f"--- SEO META DATA ---\n{f.read()}\n"

    if not context:
        print("❌ [組織連携エラー] 監査すべき原稿データまたはSEOデータが一切見つかりません。処理を中断します。")
        sys.exit(1)

    # 🔑 環境変数は一貫して「KDP_GEMINI_API_KEY」に統一
    api_key = os.environ.get("KDP_GEMINI_API_KEY")
    if not api_key:
        print("❌ [致命的エラー] 環境変数 KDP_GEMINI_API_KEY が設定されていません。")
        sys.exit(1)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
You are the Chief Legal Officer and Amazon KDP Compliance Expert for a global publishing company.
Audit the following novel manuscript and SEO metadata to ensure 100% safety against Amazon KDP bans, copyright strikes, and trademark infringements.

{context}

Analyze the text strictly based on these 4 factors:
1. **Trademark & Copyright Risk:** Check if there are any trademarked terms, or if the text too closely plagiarizes famous works (like Twilight, Harry Potter, or famous indie werewolf novels).
2. **Amazon KDP Content Guidelines:** Ensure there are no violations regarding excessive explicit violence, illegal content, or metadata spamming (keyword stuffing in titles).
3. **AI Content Disclosure Readiness:** Confirm that the formatting complies with Amazon's requirement to disclose AI-generated text if required.
4. **Final Verdict (PASS/FAIL):** Give a clear verdict. If there are any risky phrases, list them clearly and provide alternative safe phrases.

Output the entire report in English, but add a brief Japanese Executive Summary at the top for the CEO.
"""

    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
        
        if response.status_code == 429:
            print("⚠️ [API制限] Google APIのリクエスト上限(429)に達しました。")
            sys.exit(1)
            
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            
            os.makedirs(WORKSPACE_DIR, exist_ok=True)
            with open(REPORT_FILE, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"✅ Legal and compliance audit complete for Chapter {latest_chapter}. Report saved to {REPORT_FILE}.")
        else:
            print(f"❌ [APIエラー] ステータスコード: {response.status_code} - {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ [通信エラー] 監査API呼び出し中に例外が発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_compliance_check()
