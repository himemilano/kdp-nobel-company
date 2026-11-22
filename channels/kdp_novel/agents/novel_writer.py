import os
import time
import requests

class NovelWriterAgent:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY_KDP_NOBEL")
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-3.8-flash:generateContent"

    def write_chapter(self, chapter_num, plot_blueprint, previous_logs):
        system_instruction = (
            "You are a bestselling author of KDP Werewolf Romance. "
            "Write engaging, high-tension English chapters. "
            "Strictly avoid: emotional repetition, Elena acting as a passive viewer, dropping bloodline setups, and making Nicholas too soft/saintly. "
            "Maintain a balance of Nicholas's dangerous, ruthless Alpha nature and his political competence."
        )

        prompt = f"""
        [Previous Review Feedback & Must-Follow Rules]
        {previous_logs}

        [Chapter {chapter_num} Plot Blueprint]
        {plot_blueprint}

        [Instructions]
        Write Chapter {chapter_num} in English based on the blueprint.
        - Ensure Elena takes physical action (investigates, discovers, interacts).
        - Keep ancient bloodline abilities active if applicable.
        - Output ONLY the chapter text in English.
        """

        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": f"[Role]\n{system_instruction}\n\n[Task]\n{prompt}"}]}]}
        url = f"{self.base_url}?key={self.api_key}"
        
        for attempt in range(3):
            try:
                res = requests.post(url, headers=headers, json=payload, timeout=300)
                if res.status_code == 200:
                    return res.json()["candidates"][0]["content"]["parts"][0]["text"]
                print(f"Novel Writer Error: HTTP {res.status_code} {res.text[:200]}")
            except Exception as e:
                print(f"Novel Writer Error: {e}")
            if attempt < 2:
                time.sleep(20)
        return None
