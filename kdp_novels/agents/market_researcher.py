import os
import sys
import requests

WORKSPACE_DIR = "kdp_novels/workspace"
REPORT_FILE = os.path.join(WORKSPACE_DIR, "01_market_report.md")

def run_research():
    print("🕵️‍♂️ [KDP Research Dept] Starting global market trend search for Amazon.com...")
    
    # 🛡️ 【API節約ガード】すでに本日のレポートがあるなら、1文字もAPIを叩かずに即終了！
    if os.path.exists(REPORT_FILE):
        print(f"📊 [資産保護] すでに市場調査データ（{REPORT_FILE}）が存在します。既存の資産を再利用するため、本日のタスクはここで完了します（API課金 ¥0）。")
        return

    # 🔑 環境変数は一貫して「KDP_GEMINI_API_KEY」に統一
    api_key = os.environ.get("KDP_GEMINI_API_KEY")
    if not api_key:
        print("❌ [致命的エラー] 環境変数 KDP_GEMINI_API_KEY が設定されていません。処理を中断します。")
        sys.exit(1) # デモデータで誤魔化さず、エラーを検知させるために異常終了させる

    url = f""https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    prompt = (
        "Identify the top 3 high-demand, low-competition ultra-niche fiction genres on Amazon.com (US market) right now. "
        "Analyze online discussions, TikTok (BookTok) trends, Reddit r/books, and reader forums where people complain that "
        "'there aren't enough books like this' or 'I need more of this specific trope'. "
        "For each of the 3 suggestions, provide: "
        "1. Genre & Trope Name (e.g., Cozy Paranormal Mystery, Reject Werewolf Romance, Sci-Fi Age-Gap Romance) "
        "2. The Target Audience & Why they are underserved "
        "3. A unique hook or concept that a new author could immediately write to dominate this niche. "
        "Output the entire report in English, but add a brief Japanese executive summary at the very beginning for the director."
    )

    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
        
        # 429（レートリミット）などのエラーを明示的にキャッチ
        if response.status_code == 429:
            print("⚠️ [API制限] Google APIのリクエスト上限(429)に達しました。時間を空けて再試行してください。")
            sys.exit(1)
            
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            save_workspace("01_market_report.md", result)
            print("✅ Global market research report generated successfully.")
        else:
            print(f"❌ [APIエラー] ステータスコード: {response.status_code} - {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ [通信エラー] API呼び出し中に例外が発生しました: {e}")
        sys.exit(1)

def save_workspace(filename, content):
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    with open(os.path.join(WORKSPACE_DIR, filename), "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    run_research()
