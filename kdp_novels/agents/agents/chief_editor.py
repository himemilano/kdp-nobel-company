# agents/chief_editor.py
import os
import requests

class ChiefEditorAgent:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY_KDP_NOBEL")
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

    def review_chapter(self, chapter_num, chapter_text, previous_logs):
        """
        AI編集長として、最新の章を辛口に評価し、ダメ出しと修正ポイントを生成する
        """
        system_instruction = (
            "You are an elite, brutally honest Chief Editor of bestselling KDP Werewolf Romance novels. "
            "Your job is to evaluate chapters strictly based on commercial viability, pacing, mystery depth, and character agency. "
            "Never accept passive 'observation loops', forgotten bloodline setups, or unearned character saintliness."
        )

        prompt = f"""
        [Previous Review Feedback & Company Standards]
        {previous_logs}

        [Target Chapter to Review: Chapter {chapter_num}]
        {chapter_text}

        [Evaluation Instructions]
        Evaluate Chapter {chapter_num} on the following criteria:
        1. **Plot Progression**: Did the story move forward, or is it an 'observation/reflection loop'?
        2. **Protagonist Agency**: Did Elena act as a 'player' (taking initiative, investigating), or is she just a passive 'viewer'?
        3. **Bloodline & Mysteries**: Are ancient bloodline abilities or core mysteries actively functioning?
        4. **Character Balance**: Is Nicholas too soft/saintly? Is his dangerous/cruel edge properly balanced?
        5. **Hook/Cliffhanger**: Does it force the reader to open the next chapter?

        Output a strict, professional editorial review including:
        - Score (out of 100)
        - What worked well
        - Critical flaws & warnings
        - Mandatory corrections for the next chapter
        """

        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": f"[Role]\n{system_instruction}\n\n[Task]\n{prompt}"}]
            }]
        }
        
        url = f"{self.base_url}?key={self.api_key}"
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=120)
            if res.status_code == 200:
                return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Chief Editor Review Error: {e}")
        return "Review generation failed."
