import os
import time
from crewai import Agent, Task, Crew, Process, LLM

class ChiefEditorAgent:
    def __init__(self):
        # 環境変数からAPIキーを取得
        api_key = os.environ.get("GEMINI_API_KEY_KDP_NOBEL")
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
        self.api_key = api_key

    def _make_llm(self, model: str) -> LLM:
        return LLM(
            model=model,
            temperature=0.3,
            api_key=self.api_key
        )

    def editor_agent(self, llm) -> Agent:
        return Agent(
            role='総編集長 兼 クオリティ監査官',
            goal='執筆された小説の章やプロットの文脈、論理展開、表現力を厳しくチェックし、妥協のないダメ出しと具体的な改善指示を行う。',
            backstory="""あなたは大手出版社の辣腕総編集長です。
甘い評価や単なる褒め言葉は一切排除し、読者を引き込む最高品質の小説に仕上げるため、
ストーリーの矛盾、キャラクターのブレ、退屈な展開を容赦なく指摘します。
過去の監査結果やナレッジを踏まえ、次の執筆やリライトに向けた的確な「ダメ出しと改善方針」を下すのがあなたの仕事です。""",
            verbose=True,
            memory=True,
            llm=llm,
            allow_delegation=False
        )

    def review_chapter(self, chapter_num: int, chapter_text: str, previous_logs: str) -> str:
        """編集長として章の原稿を厳格に審査し、レビュー結果とダメ出しを返す"""
        # 主モデルで1回、混雑時は予備モデルで2回まで試す
        models = ["gemini/gemini-3.8-flash", "gemini/gemini-3.6-flash", "gemini/gemini-3.6-flash"]
        for attempt, model in enumerate(models):
            try:
                agent = self.editor_agent(self._make_llm(model))

                task = Task(
                    description=f"""
以下の第 {chapter_num} 章の小説原稿を厳しく審査し、改善点やダメ出し、次章への引き継ぎ事項をまとめてください。

【過去のレビュー・ダメ出し蓄積ログ】
{previous_logs}

【審査対象の原稿（第 {chapter_num} 章）】
{chapter_text}

以下の観点から厳格にチェックしてください：
1. 文脈の飛躍や矛盾がないか
2. キャラクターの言動にブレがないか
3. 過去の指摘（表現の修正や伏線の回収など）が反映されているか
""",
                    expected_output="辛口なダメ出し、良かった点、および次回に活かすべき改善指示のレポート（Markdown形式）",
                    agent=agent
                )

                crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=True
                )

                result = crew.kickoff()
                return str(result)
            except Exception as e:
                print(f"Chief Editor Error (attempt {attempt + 1}, {model}): {e}")
                if attempt < 2:
                    time.sleep(30)

        # レビューが取れなくても章本文は失わないよう、失敗を明記した注記を返す
        return f"（第{chapter_num}章の編集長レビューは、モデル側の混雑のため取得できませんでした。本文は保存されています。製本時の最終確認で要チェック。）"
