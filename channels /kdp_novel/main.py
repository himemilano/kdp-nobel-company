import os
import glob
from agents.plot_designer import PlotDesignerAgent
from agents.novel_writer import NovelWriterAgent
from agents.chief_editor import ChiefEditorAgent
from agents.legal_compliance_checker import LegalComplianceCheckerAgent
from agents.market_researcher import MarketResearcherAgent

def get_next_chapter_number():
    chapters = glob.glob("chapters/chapter_*.md")
    if not chapters:
        return 1
    nums = []
    for c in chapters:
        try:
            num = int(os.path.basename(c).replace("chapter_", "").replace(".md", ""))
            nums.append(num)
        except ValueError:
            continue
    return max(nums) + 1 if nums else 1

def main():
    print("🤖 [KDP自律統括部] システム起動: パイプラインを実行します...")
    
    # APIキー確認
    api_key = os.environ.get("GEMINI_API_KEY_KDP_NOBEL")
    if not api_key:
        raise ValueError("GEMINI_API_KEY_KDP_NOBEL environment variable is missing.")

    chapter_num = get_next_chapter_number()
    print(f"📖 ターゲット: 第 {chapter_num} 章の制作を開始します。")

    # 1. 蓄積されたレビューログとワークスペースの読み込み
    reviews_log_path = "knowledge/chapter_reviews_log.md"
    previous_logs = ""
    if os.path.exists(reviews_log_path):
        with open(reviews_log_path, "r", encoding="utf-8") as f:
            previous_logs = f.read()

    blueprint_path = "workspace/02_plot_blueprint.md"
    blueprint_context = ""
    if os.path.exists(blueprint_path):
        with open(blueprint_path, "r", encoding="utf-8") as f:
            blueprint_context = f.read()

    # 2. 各エージェントの初期化
    plot_agent = PlotDesignerAgent()
    writer_agent = NovelWriterAgent()
    editor_agent = ChiefEditorAgent()
    compliance_agent = LegalComplianceCheckerAgent()

    # 3. プロット設計
    print("✍️ [Plot Designer] プロットを設計中（観察ループ排除・血筋活性化）...")
    plot_blueprint = plot_agent.design_plot(chapter_num, f"{previous_logs}\n\n[Base Blueprint Context]\n{blueprint_context}")
    if not plot_blueprint:
        print("❌ プロット設計に失敗しました。")
        return

    # 4. 小説執筆
    print(f"✍️ [Novel Writer] 第 {chapter_num} 章を執筆中...")
    chapter_text = writer_agent.write_chapter(chapter_num, plot_blueprint, previous_logs)
    if not chapter_text:
        print("❌ 小説の執筆に失敗しました。")
        return

    # 5. 主任編集者によるダメ出し・レビュー
    print("🧐 [Chief Editor] 主任編集者が厳格に審査・ダメ出し中...")
    editor_review = editor_agent.review_chapter(chapter_num, chapter_text, previous_logs)

    # 6. コンプライアンスチェック
    print("⚖️ [Legal Compliance] リーガルチェックを実行中...")
    compliance_report = compliance_agent.check_compliance(chapter_text)

    # 7. 成果物を所定のフォルダ（chapters / workspace / knowledge）に保存
    os.makedirs("chapters", exist_ok=True)
    os.makedirs("workspace", exist_ok=True)
    os.makedirs("knowledge", exist_ok=True)

    # 小説本文の保存
    chapter_file_path = f"chapters/chapter_{chapter_num}.md"
    with open(chapter_file_path, "w", encoding="utf-8") as f:
        f.write(f"# Chapter {chapter_num}\n\n{chapter_text}")
    print(f"💾 小説原稿を保存しました: {chapter_file_path}")

    # コンプライアンス＆編集レポートの保存 (workspace/ に格納)
    report_file_path = f"workspace/05_legal_compliance_report_chapter_{chapter_num}.md"
    with open(report_file_path, "w", encoding="utf-8") as f:
        f.write(f"# Chapter {chapter_num} - Editorial & Compliance Report\n\n## Chief Editor Review\n{editor_review}\n\n## Compliance Report\n{compliance_report}")
    print(f"💾 編集・法務レポートを保存しました: {report_file_path}")

    # レビューログ（knowledge/chapter_reviews_log.md）へ今回のエディター評価を自動追記
    with open(reviews_log_path, "a", encoding="utf-8") as f:
        f.write(f"\n\n## 第{chapter_num}章 主任編集者レビュー\n{editor_review}\n")
    print(f"💾 レビューログを更新しました: {reviews_log_path}")

    print("🎉 本日のパイプライン処理が正常に完了しました。")

if __name__ == "__main__":
    main()
