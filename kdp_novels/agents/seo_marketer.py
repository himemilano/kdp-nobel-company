import os
import requests

def run_marketing():
    print("💰 [KDPマーケティング部門] Amazon KDP用・SEO最適化メタデータ及び説明文の生成開始...")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    manuscript_path = "kdp_novels/workspace/03_novel_manuscript.md"
    manuscript_context = ""
    if os.path.exists(manuscript_path):
        with open(manuscript_path, "r", encoding="utf-8") as f:
            manuscript_context = f.read()

    if not api_key:
        print("⚠️ APIキー未設定のため、SEO説明文のサンプルを配置します。")
        write_demo_seo()
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
Amazon KDPで自費出版予定の電子書籍向けに、検索SEO対策が施された書籍タイトルと、読者を購入へ誘導する説明文を日本語で作成してください。

【執筆された原稿（参考）】
{manuscript_context}

【必須要件・構成ルール】
以下の3つの要素を完璧に兼ね備えた、海外のベストセラー（例: Blue Moon Ball等）同様のフックを持つ構成にしてください：
1) ターゲット層（発達障害グレーゾーン当事者、共感系コンテンツ、日常ミステリー愛好家）が最も興奮し、感情移入する「書籍の刺激的なプレビュー部分」を冒頭に配置して開始する。
2) 読者のニッチな需要を満たし、共感を呼び起こす方法で書籍全体の魅力を説明する。
3) 対象とする具体的な検索キーワード（ニッチ市場カテゴリ）を箇条書きで分かりやすく列挙する。
"""

    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            with open("kdp_novels/workspace/04_kdp_seo_meta.md", "w", encoding="utf-8") as f:
                f.write(result)
            print("✅ Amazon KDP用・SEO最適化タイトル＆説明文が完成しました。")
        else:
            write_demo_seo()
    except Exception as e:
        print(f"エラー: {e}")
        write_demo_seo()

def write_demo_seo():
    demo = """# 💰 Amazon KDP配信用 SEO最適化データ
## 書籍タイトル案
『わたしは、謎を解いていなかった：発達障害グレーゾーン司書・谷口静の静かなる観察眼』

## 書籍説明文（Amazon商品ページ用）
「また、ズレてる。でも、あなたの嘘だけは痛いほど見えてしまう――」

空気が読めない、他人の感情の機微がわからない。そう言われ続けてきた42歳の図書館司書・谷口静。
しかし彼らが残した一筋のメモ、本の貸出履歴の奇妙な並びは、静の圧倒的な観察眼の前で「誰かの小さな困りごと」となって浮き彫りになる……。

【本書のキーワード】
- 日常系ミステリー
- 発達障害 / グレーゾーン
- 大人の生きづらさと共感
- どんでん返し
"""
    with open("kdp_novels/workspace/04_kdp_seo_meta.md", "w", encoding="utf-8") as f:
        f.write(demo)

if __name__ == "__main__":
    run_marketing()
