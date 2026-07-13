import os
import requests

def run_research():
    print("🕵️‍♂️ [KDPリサーチ部門] トレンドおよび供給不足ジャンルの探索を開始...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ APIキーが未設定のため、デモ用リサーチレポートを出力します。")
        write_demo_report()
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = (
        "Amazon KDP向けに売れる小説のジャンルを特定したいです。"
        "Yahoo!知恵袋、X（旧Twitter）、動画コメント、ネット掲示板等で人々が『こういう小説がもっと読みたいのに見つからない』『このジャンルの本が少なすぎる』と話しているような、"
        "【現在需要があるのに供給が極端に不足している超ニッチな分野・空白地帯のテーマ】を徹底的に推測・リサーチし、日本人セラーが狙うべき具体的なテーマ案を3つ提案してください。"
    )

    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            save_workspace("01_market_report.md", result)
            print("✅ リサーチレポートの自動生成が完了しました。")
        else:
            write_demo_report()
    except Exception as e:
        print(f"エラー: {e}")
        write_demo_report()

def save_workspace(filename, content):
    os.makedirs("kdp_novels/workspace", exist_ok=True)
    with open(f"kdp_novels/workspace/{filename}", "w", encoding="utf-8") as f:
        f.write(content)

def write_demo_report():
    # キーがない状態でも動くように、テンプレート例を自動格納してパイプラインを繋ぎます
    demo = """# 📊 需要あり・供給不足の超ニッチジャンルリサーチ報告書
## ターゲット選定：発達障害グレーゾーン×日常ミステリー
- **背景:** エッセイや実録本は増えているが、彼らを魅力的な主人公に据えた「日常系ミステリー小説」の選択肢が極めて少なく、強い共感需要がある。
"""
    save_workspace("01_market_report.md", demo)

if __name__ == "__main__":
    run_research()
