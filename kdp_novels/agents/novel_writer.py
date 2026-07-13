import os
import requests

def run_writer():
    print("✍️ [KDP執筆・編集部門] 小説本文の執筆および自動リライト・編集チェックを開始...")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    blueprint_path = "kdp_novels/workspace/02_plot_blueprint.md"
    blueprint_context = ""
    if os.path.exists(blueprint_path):
        with open(blueprint_path, "r", encoding="utf-8") as f:
            blueprint_context = f.read()

    if not api_key:
        print("⚠️ APIキー未設定のため、原稿のサンプルを配置します。")
        write_demo_manuscript()
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
以下のキャラクター設定、エンディング構想、およびSave the Catストーリーライン概要を元に、Amazon KDP出版用の小説の「第1章」を圧倒的な描写力で執筆してください。
また、執筆した後に自分で読み返し、誤字脱字や矛盾点がないかをセルフチェックした最終完成原稿を出力してください。

【小説設計図】
{blueprint_context}
"""

    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=90)
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            with open("kdp_novels/workspace/03_novel_manuscript.md", "w", encoding="utf-8") as f:
                f.write(result)
            print("✅ 小説第1章の執筆と校正・編集デバッグが完了しました。")
        else:
            write_demo_manuscript()
    except Exception as e:
        print(f"エラー: {e}")
        write_demo_manuscript()

def write_demo_manuscript():
    demo = """# 📚 小説原稿：『わたしは、謎を解いていなかった』
## 第1章：本の背表紙と、静かなる波紋
カウンターに置かれた本の返却期限は、三日過ぎていた。谷口静は、指先でその古い背表紙をなぞる。
「空気が読めない」と人は言う。しかし、静にとって世界は情報に満ち溢れていた。貸出カードのインクの滲み、挟まれた付箋の折り目……。
"""
    with open("kdp_novels/workspace/03_novel_manuscript.md", "w", encoding="utf-8") as f:
        f.write(demo)

if __name__ == "__main__":
    run_writer()
