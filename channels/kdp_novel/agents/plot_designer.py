import os
import time
import requests

FINALE_START_CHAPTER = 52


class PlotDesignerAgent:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY_KDP_NOBEL")
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-3.8-flash:generateContent"
        self.fallback_url = "https://generativelanguage.googleapis.com/v1/models/gemini-3.6-flash:generateContent"

    def design_plot(self, chapter_num, previous_logs):
        if chapter_num >= FINALE_START_CHAPTER:
            system_instruction = (
                "You are an expert Plot Architect for bestselling KDP Werewolf Romance novels. "
                "You are designing the CLOSING chapters of the book. The [Base Blueprint Context] "
                "at the end of the context is the binding finale design and OVERRIDES every other "
                "rule in this prompt, including any earlier cliffhanger habit. Chapters 52-54 must "
                "each END RESOLVED: no cliffhanger, no new threat, no escalation. Chapter 55 is the "
                "epilogue and must close the book."
            )

            prompt = f"""
        [Previous Review Feedback & Strict Rules]
        {previous_logs}

        [Task]
        Design a detailed plot blueprint for Chapter {chapter_num} EXACTLY following the finale design
        in the [Base Blueprint Context] above. Do NOT add new settings, powers, entities, or named
        concepts. Do NOT escalate the conflict. The chapter must END RESOLVED (Chapter 55: end as a
        quiet epilogue that closes the book). Do NOT write a cliffhanger.
        """
        else:
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
        urls = [f"{self.base_url}?key={self.api_key}", f"{self.fallback_url}?key={self.api_key}"]
        
        for attempt in range(4):
            try:
                res = requests.post(urls[min(attempt // 2, 1)], headers=headers, json=payload, timeout=300)
                if res.status_code == 200:
                    return res.json()["candidates"][0]["content"]["parts"][0]["text"]
                print(f"Plot Designer Error: HTTP {res.status_code} {res.text[:200]}")
            except Exception as e:
                print(f"Plot Designer Error: {e}")
            if attempt < 3:
                time.sleep(20)
        return None
