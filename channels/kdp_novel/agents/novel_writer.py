import os
import time
import requests

FINALE_START_CHAPTER = 52


class NovelWriterAgent:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY_KDP_NOBEL")
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-3.8-flash:generateContent"
        self.fallback_url = "https://generativelanguage.googleapis.com/v1/models/gemini-3.6-flash:generateContent"

    def write_chapter(self, chapter_num, plot_blueprint, previous_logs):
        if chapter_num >= FINALE_START_CHAPTER:
            system_instruction = (
                "You are a bestselling author of KDP Werewolf Romance. "
                "You are writing the CLOSING chapters of the book. The chapter plot blueprint is "
                "binding: follow it exactly. Chapters 52-54 must each END RESOLVED: no cliffhanger, "
                "no new threat, no escalation. Chapter 55 is the epilogue and must close the book "
                "with a quiet, resolved ending."
            )

            prompt = f"""
        [Previous Review Feedback & Must-Follow Rules]
        {previous_logs}

        [Chapter {chapter_num} Plot Blueprint]
        {plot_blueprint}

        [Instructions]
        Write Chapter {chapter_num} in English based on the blueprint.
        - Follow the blueprint exactly. Do NOT add a cliffhanger or a new threat.
        - Ensure Elena takes physical action (investigates, discovers, interacts).
        - Keep ancient bloodline abilities active if applicable.
        - The chapter must END RESOLVED (Chapter 55: end as a quiet epilogue that closes the book).
        - Output ONLY the chapter text in English.
        """
        else:
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
        urls = [f"{self.base_url}?key={self.api_key}", f"{self.fallback_url}?key={self.api_key}"]
        
        for attempt in range(4):
            try:
                res = requests.post(urls[min(attempt // 2, 1)], headers=headers, json=payload, timeout=300)
                if res.status_code == 200:
                    return res.json()["candidates"][0]["content"]["parts"][0]["text"]
                print(f"Novel Writer Error: HTTP {res.status_code} {res.text[:200]}")
            except Exception as e:
                print(f"Novel Writer Error: {e}")
            if attempt < 3:
                time.sleep(20)
        return None
