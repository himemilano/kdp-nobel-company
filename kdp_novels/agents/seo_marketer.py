import os
import requests

class SeoMarketerAgent:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY_KDP_NOBEL")
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

    def optimize_meta(self, story_summary):
        system_instruction = (
            "You are an expert KDP SEO and Copywriting Marketer. "
            "Create high-converting book descriptions, subtitles, and backend keywords for Werewolf Romance novels."
        )

        prompt = f"""
        [Story Summary]
        {story_summary}

        [Task]
        Generate compelling KDP metadata, including SEO-optimized subtitles, backend keywords, and a high-converting book description that hooks romance readers.
        """

        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": f"[Role]\n{system_instruction}\n\n[Task]\n{prompt}"}]}]}
        url = f"{self.base_url}?key={self.api_key}"
        
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=120)
            if res.status_code == 200:
                return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"SEO Marketer Error: {e}")
        return None
