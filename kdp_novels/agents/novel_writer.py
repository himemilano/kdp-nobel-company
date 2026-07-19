import os
import sys
import glob
import re
import requests

WORKSPACE_DIR = "kdp_novels/workspace"
BLUEPRINT_FILE = os.path.join(WORKSPACE_DIR, "02_plot_blueprint.md")

def determine_next_chapter():
    """📁 既存の執筆済みファイルをスキャンして、次に書くべき章番号を割り出す"""
    search_pattern = os.path.join(WORKSPACE_DIR, "03_novel_manuscript_chapter_*.md")
    files = glob.glob(search_pattern)
    
    max_chapter = 0
    for file in files:
        match = re.search(r'chapter_(\d+)\.md', file)
        if match:
            max_chapter = max(max_chapter, int(match.group(1)))
            
    # 旧形式（03_novel_manuscript.md）が残っている場合は1章とみなす
    if max_chapter == 0 and os.path.exists(os.path.join(WORKSPACE_DIR, "03_novel_manuscript.md")):
        return 2
        
    return max_chapter + 1

def get_previous_context(current_chapter):
    """🧠 直前のチャプターの終盤の文脈を読み込み、話の繋がりを保証する"""
    if current_chapter == 1:
        return ""
        
    prev_chapter = current_chapter - 1
    # 旧形式または連番形式のファイルパスを確認
    prev_file = os.path.join(WORKSPACE_DIR, f"03_novel_manuscript_chapter_{prev_chapter}.md")
    if prev_chapter == 1 and os.path.exists(os.path.join(WORKSPACE_DIR, "03_novel_manuscript.md")):
        prev_file = os.path.join(WORKSPACE_DIR, "03_novel_manuscript.md")
        
    if os.path.exists(prev_file):
        with open(prev_file, "r", encoding="utf-8") as f:
            content = f.read()
            # 直前の繋がりを保つため、前章の「後半2000文字」をコンテキストとして抽出
            return f"\n\n--- [Story so far: Chapter {prev_chapter} Ending Part] ---\n{content[-2000:]}"
    return ""

def run_writer():
    # 🔗 【バトンチェック】プロット設計図があるか確認
    if not os.path.exists(BLUEPRINT_FILE):
        print(f"❌ [組織連携エラー] 前段のプロット設計図（{BLUEPRINT_FILE}）が見つかりません。中断します。")
        sys.exit(1)

    with open(BLUEPRINT_FILE, "r", encoding="utf-8") as f:
        blueprint_context = f.read()

    # 🔢 次に執筆すべき章を自動決定
    next_chapter = determine_next_chapter()
    
    # 🛡️ 【API節約ガード】Save the Catの15ビート（15章）を書き終えているなら即退勤
    if next_chapter > 15:
        print(f"🎉 [全章執筆完了] すでに第15章まで原稿が存在します。本日の執筆タスクはありません（API課金 ¥0）。")
        return

    TARGET_MANUSCRIPT_FILE = os.path.join(WORKSPACE_DIR, f"03_novel_manuscript_chapter_{next_chapter}.md")
    print(f"✍️ [KDP Writing Dept] Automating Novel Progress... Target: 【Chapter {next_chapter}】")

    # 🔑 環境変数チェック
    api_key = os.environ.get("KDP_GEMINI_API_KEY")
    if not api_key:
        print("❌ [致命的エラー] 環境変数 KDP_GEMINI_API_KEY が設定されていません。")
        sys.exit(1)

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    # 🧠 前の章の記憶をサルベージ
    history_context = get_previous_context(next_chapter)

    prompt = f"""
Using the following character profiles, chosen ending, and Save the Cat storyline blueprint:
{blueprint_context}

{history_context}

Write "Chapter {next_chapter}" of this novel in English. 
Ensure the writing style is highly immersive, filled with deep sensory details, emotional tension, and compelling dialogue that matches the highest-selling US fiction on Amazon KDP.
Proceed naturally from where the previous story left off (if any context is provided above).
Write at least 600-1000 words of high-quality storytelling. Do NOT write meta-text, commentary, or introduction like "Here is Chapter X". Start directly with the story.
"""

    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=120)
        
        if response.status_code == 429:
            print("⚠️ [API制限] Google APIのリクエスト上限(429)に達しました。")
            sys.exit(1)
            
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            
            os.makedirs(WORKSPACE_DIR, exist_ok=True)
            with open(TARGET_MANUSCRIPT_FILE, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"✅ 【Chapter {next_chapter}】 successfully written and saved to {TARGET_MANUSCRIPT_FILE}.")
        else:
            print(f"❌ [APIエラー] ステータスコード: {response.status_code} - {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ [通信エラー] 執筆API呼び出し中に例外が発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_writer()
