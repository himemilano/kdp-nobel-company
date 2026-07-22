import os
import requests

class LegalComplianceCheckerAgent:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY_KDP_NOBEL")
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"

    def check_compliance(self, text_content):
        system_instruction = (
            "You are a strict Legal & Content Compliance Officer for Amazon KDP publications. "
            "Ensure the manuscript adheres strictly to platform safety guidelines while preserving creative dark romance elements."
        )

        prompt = f"""
        [Target Text]
        {text_content}

        [Task]
        Review the text for any KDP policy violations. Report any issues and suggest safe, compliant phrasings if necessary.
        """

        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": f"[Role]\n{system_instruction}\n\n[Task]\n{prompt}"}]}]}
        url = f"{self.base_url}?key={self.api_key}"
        
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=120)
            if res.status_code == 200:
                return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Compliance Checker Error: {e}")
        return None

