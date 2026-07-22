import os
import requests

class MarketResearcherAgent:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY_KDP_NOBEL")
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

    def analyze_market(self):
        system_instruction = (
            "You are an expert KDP Market Analyst specializing in Werewolf Romance and Paranormal Mystery tropes. "
            "Identify what keeps readers turning pages: forced proximity, rejected mates, hidden bloodlines, and political conspiracies."
        )

        prompt = "Analyze current KDP trends for Werewolf Romance and provide strategic insights for maintaining high reader retention and page-turner tension."

        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": f"[Role]\n{system_instruction}\n\n[Task]\n{prompt}"}]}]}
        url = f"{self.base_url}?key={self.api_key}"
        
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=120)
            if res.status_code == 200:
                return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Market Researcher Error: {e}")
        return None
