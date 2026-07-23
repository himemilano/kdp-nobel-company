import os
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

class ChiefEditorAgent:
    def __init__(self):
        # 環境変数からAPIキーを取得
        api_key = os.environ.get("GEMINI_API_KEY_KDP_NOBEL")
        
        # Geminiモデルの設定
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            google_api_key=api_key
        )

    def editor_agent(self) -> Agent:
        return Agent(
            role='総編集長 兼 クオリティ監査官',
            goal='執筆された小説の章やプロットの文脈、論理展開、表現力を厳しくチェックし、妥協のないダメ出しと具体的な改善指示を行う。',
            backstory="""あなたは大手出版社の辣腕総編集長です。
甘い評価や単なる褒め言葉は一切排除し、読者を引き込む最高品質の小説に仕上げるため、
ストーリーの矛盾、キャラクターのブレ、退屈な展開を容赦なく指摘します。
過去の監査結果やナレッジを踏まえ、次の執筆やリライトに向けた的確な「ダメ出しと改善方針」を下すのがあなたの仕事です。""",
            verbose=True,
            memory=True,
            llm=self.llm,
            allow_delegation=False
        )

