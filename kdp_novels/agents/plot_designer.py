import os
import requests

def run_plot_design():
    print("📐 [KDPプロット構成部門] キャラクター設計およびSave the Cat構成案の構築開始...")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # 前ステップのリサーチ結果を読み込む
    report_path = "kdp_novels/workspace/01_market_report.md"
    market_context = ""
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            market_context = f.read()

    if not api_key:
        print("⚠️ APIキー未設定のため、設計図の初期テンプレートを配置します。")
        write_demo_blueprint()
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
以下のリサーチ情報をベースに、Amazon KDP用のニッチ小説のプロットを完全設計してください。
【市場リサーチ情報】
{market_context}

以下のステップをすべて網羅して1つのドキュメントにまとめてください：
1. 読者が楽しめる「10種類の異なるエンディング案」の提示と、その中から最も構成力で勝負できる「どんでん返し系」のオチの決定・詳細展開。
2. 主人公（35〜50歳の図書館司書、発達障害グレーゾーンの女性、空気が読めないが観察眼が鋭い）および主要登場人物のプロフィールと詳細な「外見の説明」。
3. ハリウッドの脚本術「セーブ・ザ・キャット方式（Save the Cat）」の15段階形式に基づき、章ごとに分割したブレイクダウン形式のストーリーラインアウトラインの作成。
"""

    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            with open("kdp_novels/workspace/02_plot_blueprint.md", "w", encoding="utf-8") as f:
                f.write(result)
            print("✅ 登場人物設定およびストーリーライン設計図（Save the Cat）が確定しました。")
        else:
            write_demo_blueprint()
    except Exception as e:
        print(f"エラー: {e}")
        write_demo_blueprint()

def write_demo_blueprint():
    demo = """# 📐 小説設計図（プロット＆キャラクタープロフィール）
## エンディング：『わたしは、謎を解いていなかった』（どんでん返し系）
## 登場人物:
- **谷口 静 (42)** / 図書館司書。髪は無造作にまとめ、度の強い眼鏡。観察眼が鋭い。
## ストーリーライン（Save the Cat 15段階）:
- 第1章（オープニングイメージ〜テーマの提示）...
"""
    with open("kdp_novels/workspace/02_plot_blueprint.md", "w", encoding="utf-8") as f:
        f.write(demo)

if __name__ == "__main__":
    run_plot_design()
