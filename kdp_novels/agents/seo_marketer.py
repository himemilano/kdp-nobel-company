import os
import sys
import requests

WORKSPACE_DIR = "kdp_novels/workspace"
BLUEPRINT_FILE = os.path.join(WORKSPACE_DIR, "02_plot_blueprint.md")
SEO_FILE = os.path.join(WORKSPACE_DIR, "04_kdp_seo_meta.md")

def run_marketing():
    print("💰 [KDP Marketing Dept] Generating global SEO metadata & English book description...")
    
    # 🛡️ 【API節約ガード】すでにSEOメタデータがあるなら、1文字もAPIを叩かずに即終了！
    if os.path.exists(SEO_FILE):
        print(f"💰 [資産保護] すでにSEOメタデータ（{SEO_FILE}）が存在します。既存の資産を再利用するため、即時退勤します（API課金 ¥0）。")
        return

    # 🔗 【バトンチェック】物語の全体像がわかるプロット設計図があるか確認
    if not os.path.exists(BLUEPRINT_FILE):
        print(f"❌ [組織連携エラー] 核心となるプロット設計図（{BLUEPRINT_FILE}）が見つかりません。中断します。")
        sys.exit(1)

    with open(BLUEPRINT_FILE, "r", encoding="utf-8") as f:
        blueprint_context = f.read()

    # 🔑 環境変数は一貫して「KDP_GEMINI_API_KEY」に統一
    api_key = os.environ.get("KDP_GEMINI_API_KEY")
    if not api_key:
        print("❌ [致命的エラー] 環境変数 KDP_GEMINI_API_KEY が設定されていません。")
        sys.exit(1)

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    # 🌟 人狼固定を排除し、どんなニッチジャンルにも適応するプロンプトへ修正
    prompt = f"""
Create a highly optimized book title, subtitle, and an extremely compelling book description in English for the Amazon.com (US KDP store) based on the following novel blueprint and plot details:
{blueprint_context}

Your output must strictly follow the 3-part blueprint of top-selling books in this specific niche on Amazon:
1) **The Hook (First lines):** Write a dramatic, emotional, or sensory-heavy opening teaser to capture the reader's attention instantly. Use short, punchy paragraphs.
2) **The Description:** Describe the plot in a way that creates extreme tension, emphasizing the core tropes and high-concept hooks of the project to trigger the reader's emotional buying impulse.
3) **Niche & Keywords list:** Add a clean list of highly searched tropes/keywords at the end (e.g., ✔️ Chosen Trope 1, ✔️ Chosen Trope 2) to dominate KDP search rankings.

The entire output must be in English.
"""

    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
        
        if response.status_code == 429:
            print("⚠️ [API制限] Google APIのリクエスト上限(429)に達しました。")
            sys.exit(1)
            
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            
            os.makedirs(WORKSPACE_DIR, exist_ok=True)
            with open(SEO_FILE, "w", encoding="utf-8") as f:
                f.write(result)
            print("✅ Amazon US KDP SEO title and book description successfully generated based on the blueprint.")
        else:
            print(f"❌ [APIエラー] ステータスコード: {response.status_code} - {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ [通信エラー] マーケティングAPI呼び出し中に例外が発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_marketing()
