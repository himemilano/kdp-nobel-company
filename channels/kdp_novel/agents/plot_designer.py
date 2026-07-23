import os
import requests

class PlotDesignerAgent:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY_KDP_NOBEL")
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

    def design_plot(self, chapter_num, previous_logs):
        system_instruction = (
            "You are an expert Plot Architect for bestselling KDP Werewolf Romance novels. "
            "Your core rule is to FORBID passive observation loops ('walk into forest -> hunt -> smell Alpha -> reminisce -> resolve'). "
            "Every chapter plot must feature: 1) Active plot progression, 2) Elena acting as a player (investigating, confronting), "
            "3) Ancient bloodline activation, and 4) Strong hooks/cliffhangers."
        )

        prompt = f"""
        [Previous Review Feedback & Strict Rules]
        {previous_logs}

        [Task]
        Design a detailed plot blueprint for Chapter {chapter_num}. 
        Ensure it does NOT repeat the observation loop. Include:
        - Specific external events or clues (e.g., Serpent mark, treaty violations).
        - Elena's proactive investigative actions.
        - Ancient bloodline/ability triggers.
        - A gripping cliffhanger that forces the reader to open the next chapter.
        """

        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": f"[Role]\n{system_instruction}\n\n[Task]\n{prompt}"}]}]}
        url = f"{self.base_url}?key={self.api_key}"
        
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=120)
            if res.status_code == 200:
                return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Plot Designer Error: {e}")
        return None

