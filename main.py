import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta, timezone

# ==========================================================
# ⚙️ 1. 設定・ディレクトリ構成
# ==========================================================
jst = timezone(timedelta(hours=9))
WORKSPACE_DIR = "kdp_novels/workspace"
os.makedirs(WORKSPACE_DIR, exist_ok=True)

class KDPNovelMasterSystem:
    """市場のゆがみを自律リサーチし、選定された任意のニッチジャンルに合わせた小説執筆を連動させる"""
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    def ask_gemini(self, prompt, system_instruction=""):
        if not self.api_key:
            return "⚠️ API KEY IS MISSING"
            
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": system_instruction}]}
        }
        url = f"{self.base_url}?key={self.api_key}"
        
        # 指数バックオフ
        for delay in [1, 2, 4]:
            try:
                res = requests.post(url, headers=headers, json=payload, timeout=90)
                if res.status_code == 200:
                    return res.json()["candidates"][0]["content"]["parts"][0]["text"]
                elif res.status_code == 429:
                    print(f"⚠️ Google API制限 (429 RESOURCE_EXHAUSTED)。残高またはクォータを確認してください。{delay}秒後にリトライします...")
                    time.sleep(delay)
                else:
                    print(f"⚠️ APIレスポンスエラー (Status: {res.status_code}): {res.text}")
                    return f"⚠️ API Error: {res.status_code}"
            except Exception as e:
                print(f"⚠️ 通信接続エラー: {e}")
                time.sleep(delay)
        return "⚠️ API Connection Failed after retries"

    def determine_next_chapter(self):
        """📁 現在の進捗（Chapter数）をスキャンして自動連番にする"""
        chapter_num = 1
        while True:
            file_name = f"03_novel_manuscript_chapter_{chapter_num}.md"
            if chapter_num == 1 and os.path.exists(os.path.join(WORKSPACE_DIR, "03_novel_manuscript.md")):
                chapter_num = 2
                continue
                
            if os.path.exists(os.path.join(WORKSPACE_DIR, file_name)):
                chapter_num += 1
            else:
                break
        return chapter_num

    def execute_pipeline(self):
        print(f"🕵️‍♂️ [KDP自律統括部] 本日の自律パトロール＆ハッキングタスクを開始します。")
        
        # 🧪 1. 完全自律型「需要と供給のゆがみ」リサーチ
        research_file = os.path.join(WORKSPACE_DIR, "01_market_report.md")
        if not os.path.exists(research_file):
            print("📊 [自律分析] 米国Amazon KDP市場の『需要と供給の歪み』をリアルにハック中...")
            prompt = (
                "Identify the top 3 high-demand, low-competition ultra-niche fiction genres/tropes on Amazon.com (US KDP market) right now. "
                "Analyze online trends, reader complaints ('not enough books like this'), and underserved sub-genres (e.g., Cozy Fantasy, Sci-Fi Romance, Cyberpunk Thriller, Speculative Fiction, Dark Academia). "
                "For each of the 3 suggestions, provide: "
                "1. Niche Genre & Core Trope "
                "2. The Target Audience & Why they are underserved "
                "3. A unique hook or concept to dominate this niche. "
                "Then, select the SINGLE most profitable, underserved niche to proceed with and explain why you chose it. "
                "The entire report must be in English with a brief Japanese executive summary at the very beginning."
            )
            report = self.ask_gemini(prompt, "You are a professional KDP Publisher.")
            
            # APIエラー時はプロセスをクラッシュさせずに安全に終了（無駄な課金と進行を防止）
            if "⚠️" in report:
                print(f"🛑 [APIエラー検知] リサーチ段階でエラーが発生しました。これ以上の課金リクエストを防止するため、安全に処理を停止し、現状を維持して退勤します。")
                return True # 正常終了扱いにしてコミット処理へ繋ぐ
                
            with open(research_file, "w", encoding="utf-8") as f:
                f.write(report)
            print("✅ 01_market_report.md を生成し、即座に保存しました。")
        else:
            print("📊 [スキップ] 既に市場調査データ(01_market_report.md)が存在します。既存の資産を再利用します（API課金 ¥0）。")

        # 🪐 2. 任意のニッチジャンルに基づいたプロット設計（Save the Cat! 15ビート）
        blueprint_file = os.path.join(WORKSPACE_DIR, "02_plot_blueprint.md")
        if not os.path.exists(blueprint_file):
            print("📐 リサーチに基づき、プロット設計図を新規作成します...")
            with open(research_file, "r", encoding="utf-8") as f:
                research_data = f.read()
            prompt = f"""
Based on the following custom market report:
{research_data}

Design a completely original, highly addictive fiction project targeting the SELECTED UNDERSERVED NICHE from the report. Do NOT assume werewolf romance unless it was explicitly selected in the report.
Generate a comprehensive blueprint containing:
1. Core Novel Information (Selected Niche, Genre, High-Concept Hook)
2. Character Profiles (Protagonist, Antagonist, Supporting Cast with desires, flaws, and secrets)
3. Save the Cat! 15-Beat Storyline: Map out a detailed 15-chapter outline based on the 15-beat structure tailored perfectly to this specific genre.
The entire output must be in English.
"""
            blueprint = self.ask_gemini(prompt, "You are an expert novelist outline designer.")
            
            if "⚠️" in blueprint:
                print(f"🛑 [APIエラー検知] プロット作成段階でエラーが発生しました。前段の市場調査データは既に安全に保存されています。ここで安全に処理を中断します。")
                return True
                
            with open(blueprint_file, "w", encoding="utf-8") as f:
                f.write(blueprint)
            print("✅ 02_plot_blueprint.md を生成し、即座に保存しました。")
        else:
            print("📐 [スキップ] 既にプロット設計図(02_plot_blueprint.md)が存在します。既存の資産を再利用します（API課金 ¥0）。")

        # ✍️ 3. 動的プロットに追従する「自動連番執筆」
        next_chapter = self.determine_next_chapter()
        print(f"✍️ 現在の執筆進捗を解析。本日執筆すべきターゲット: 【Chapter {next_chapter}】")
        
        with open(blueprint_file, "r", encoding="utf-8") as f:
            blueprint_data = f.read()
            
        previous_chapters_context = ""
        for i in range(1, next_chapter):
            prev_file = f"03_novel_manuscript_chapter_{i}.md"
            if i == 1 and os.path.exists(os.path.join(WORKSPACE_DIR, "03_novel_manuscript.md")):
                prev_file = "03_novel_manuscript.md"
            
            p_path = os.path.join(WORKSPACE_DIR, prev_file)
            if os.path.exists(p_path):
                with open(p_path, "r", encoding="utf-8") as pf:
                    previous_chapters_context += f"\n\n--- [Chapter {i} Story so far] ---\n" + pf.read()[:800]

        prompt = f"""
Using the following plot blueprint (which outlines the unique genre and characters):
{blueprint_data}

{previous_chapters_context}

Write "Chapter {next_chapter}" of this novel in English.
Make it highly immersive, filled with emotional tension, deep sensory details, and vivid character dialogue suitable for top-selling Amazon US KDP fiction in this specific niche.
Write at least 500-800 words of high-quality storytelling. Proceed naturally from where the previous story left off. Do NOT write meta-text or commentary.
"""
        new_manuscript = self.ask_gemini(prompt, "You are a bestselling novelist on Amazon KDP.")
        
        if "⚠️" in new_manuscript:
            print(f"🛑 [APIエラー検知] 【Chapter {next_chapter}】の執筆中にエラーが発生しました。本日分の執筆は安全にスキップし、前段までの進捗をコミットして正常退勤します。")
            return True

        new_chapter_file = os.path.join(WORKSPACE_DIR, f"03_novel_manuscript_chapter_{next_chapter}.md")
        with open(new_chapter_file, "w", encoding="utf-8") as f:
            f.write(new_manuscript)
        print(f"✅ 【Chapter {next_chapter}】の執筆が正常完了し、即座にディスクへ保存しました！ -> {new_chapter_file}")

        # 💰 4. 動的ジャンルに対応した KDP SEO メタ
        seo_file = os.path.join(WORKSPACE_DIR, "04_kdp_seo_meta.md")
        print("💰 Amazon KDP用のSEOタイトル、説明文、検索キーワード一覧を自動生成/更新します...")
        prompt = f"Create highly attractive, HTML-formatted Book Description, 7 KDP Search Keywords, and Subtitle based on this chapter:\n{new_manuscript[:1500]}"
        seo_meta = self.ask_gemini(prompt, "You are a professional KDP SEO Marketer.")
        
        if "⚠️" in seo_meta:
            print(f"🛑 [APIエラー検知] SEOメタデータの生成のみスキップされました。しかし、本日の核心である小説原稿【Chapter {next_chapter}】は100%安全に保存されています。")
            return True
            
        with open(seo_file, "w", encoding="utf-8") as f:
            f.write(seo_meta)
        print("✅ 04_kdp_seo_meta.md を更新・保存しました。")
        return True

def main():
    # 🔑 KDP専用の唯一のAPIキー環境変数（KDP_GEMINI_API_KEY）のみを取得します
    api_key = os.getenv("KDP_GEMINI_API_KEY")
        
    if not api_key:
        print("❌ APIキーが取得できません。環境変数 KDP_GEMINI_API_KEY を確認してください。")
        sys.exit(1)

    system = KDPNovelMasterSystem(api_key=api_key)
    
    try:
        success = system.execute_pipeline()
        if not success:
            print("⚠️ 執筆プロセスの完了を検知できませんでした。")
    except Exception as e:
        # プログラム側の予期せぬ例外バグでも、それまでに作成された成果物はコミットプッシュされるように保護
        print(f"❌ システム実行中に重大なエラーが発生しました: {e}")
        print("💡 しかし、これまでに生成されたファイル（01〜03）はディスクに安全に保持されています。")

if __name__ == "__main__":
    main()
