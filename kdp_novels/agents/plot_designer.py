import os
import sys
import requests

WORKSPACE_DIR = "kdp_novels/workspace"
REPORT_FILE = os.path.join(WORKSPACE_DIR, "01_market_report.md")
BLUEPRINT_FILE = os.path.join(WORKSPACE_DIR, "02_plot_blueprint.md")

def run_plot_design():
    print("📐 [KDP Plot Design Dept] Generating global character profile and Save the Cat outline...")
    
    # 🛡️ 【API節約ガード】すでにプロット設計図があるなら、1文字もAPIを叩かずに即終了！
    if os.path.exists(BLUEPRINT_FILE):
        print(f"📐 [資産保護] すでにプロット設計図（{BLUEPRINT_FILE}）が存在します。既存の資産を再利用するため、即時退勤します（API課金 ¥0）。")
        return

    # 🔗 【バトンチェック】前段の市場調査レポートがあるか確認
    if not os.path.exists(REPORT_FILE):
        print(f"❌ [組織連携エラー] 前段の市場調査レポート（{REPORT_FILE}）が見つかりません。リレーを中断します。")
        sys.exit(1)

    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        market_context = f.read()

    # 🔑 環境変数は一貫して「GEMINI_API_KEY_KDP_NOBEL」に統一
    api_key = os.environ.get("GEMINI_API_KEY_KDP_NOBEL")
    if not api_key:
        print("❌ [致命的エラー] 環境変数 KDP_GEMINI_API_KEY が設定されていません。処理を中断します。")
        sys.exit(1)

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
Based on the following global market research report:
{market_context}

Design a completely original, highly addictive fiction project targeting the Amazon.com US market. Do NOT copy any existing examples.
Generate a comprehensive blueprint containing:
1. **The Ultimate Ending (10 variants):** Brainstorm 10 different, highly satisfying or mind-blowing endings tailored to this niche. Then, select the most powerful, emotional, or plot-twist ending and explain how it will be fully executed.
2. **Character Profiles:** Create detailed profiles for the main characters (including physical appearance, inner flaws, desires, and secrets). Ensure they perfectly appeal to the target readers.
3. **Save the Cat! 15-Beat Storyline:** Create a detailed 15-beat outline of the novel, broken down by chapter. Every beat must build maximum emotional tension and hook the reader to turn the next page.

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
            with open(BLUEPRINT_FILE, "w", encoding="utf-8") as f:
                f.write(result)
            print("✅ Global blueprint and Save the Cat outline successfully generated.")
        else:
            print(f"❌ [APIエラー] ステータスコード: {response.status_code} - {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ [通信エラー] API呼び出し中に例外が発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_plot_design()
