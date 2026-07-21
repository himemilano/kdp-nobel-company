import os
import sys
import requests

# API設定
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY_MEDIA")
BASE_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

def ask_gemini(prompt, system_instruction=""):
    if not GEMINI_API_KEY:
        print("❌ エラー: GEMINI_API_KEY_MEDIA が設定されていません。")
        return None
    headers = {"Content-Type": "application/json"}
    combined_prompt = f"[Role Instruction]\n{system_instruction}\n\n[Task]\n{prompt}" if system_instruction else prompt
    payload = {"contents": [{"parts": [{"text": combined_prompt}]}]}
    url = f"{BASE_URL}?key={GEMINI_API_KEY}"
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=120)
        if res.status_code == 200:
            return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Gemini API Error: {e}")
    return None

def load_file(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def save_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def run_rewrite_pipeline(target_chapter_num=2):
    print(f"🐺 [KDP Novel Engine] 第{target_chapter_num}章 リライト・自動矯正モード起動")
    
    # 1. ナレッジと原稿のロード（.md形式に対応）
    genre_rules = load_file("knowledge/genre_rules.md")
    reviews_log = load_file("knowledge/chapter_reviews_log.md")
    chapter_path = f"chapters/chapter_{target_chapter_num:02d}.md"
    original_text = load_file(chapter_path)
    
    if not original_text:
        print(f"❌ 対象の章ファイルが見つかりません: {chapter_path}")
        return False

    # 2. プロンプトの構築（ナレッジを完全にインジェクト）
    system_instruction = (
        "You are an expert Chief Editor and bestselling author of KDP Werewolf Romance novels. "
        "Your task is to rewrite and elevate the given chapter based strictly on the provided Genre Rules and Previous Review Feedback. "
        "Ensure new facts, an active incident, and a strong cliffhanger are included, while eliminating emotional repetition."
    )
    
    prompt = f"""
    [Genre Rules & Standards]
    {genre_rules}
    
    [Previous Review Feedback & Mistakes to Avoid]
    {reviews_log}
    
    [Original Draft of Chapter {target_chapter_num}]
    {original_text}
    
    [Instructions]
    Rewrite this chapter in English to fully address all review feedback. 
    - Make sure the plot moves forward (add an incident/new info, such as Rafe's overheard conversation).
    - Fix any logic gaps, pacing issues, or lack of new information.
    - Keep the high-quality commercial tone of a bestselling Werewolf Romance.
    - Output ONLY the revised chapter text in English. Do not include conversational filler.
    """

    print("✍️ AI編集部によるリライトを実行中...")
    revised_text = ask_gemini(prompt, system_instruction)
    
    if not revised_text:
        print("❌ リライトの生成に失敗しました。")
        return False

    # 3. 成果物の保存（.md形式に対応）
    backup_path = f"chapters/chapter_{target_chapter_num:02d}_backup.md"
    save_file(backup_path, original_text)  # 元の原稿のバックアップ
    save_file(chapter_path, revised_text)  # リライト版を上書き保存
    
    print(f"✅ 第{target_chapter_num}章のリライトが完了し、{chapter_path} に保存されました！")
    print(f"📁 元の原稿は {backup_path} にバックアップされています。")
    return True

if __name__ == "__main__":
    success = run_rewrite_pipeline(target_chapter_num=2)
    if not success:
        sys.exit(1)
