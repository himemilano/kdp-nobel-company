import os
import requests

def run_research():
    print("🕵️‍♂️ [KDP Research Dept] Starting global market trend search for Amazon.com...")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ API Key not found. Generating default global market report...")
        write_demo_report()
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = (
        "Identify the top 3 high-demand, low-competition ultra-niche fiction genres on Amazon.com (US market) right now. "
        "Analyze online discussions, TikTok (BookTok) trends, Reddit r/books, and reader forums where people complain that "
        "'there aren't enough books like this' or 'I need more of this specific trope'. "
        "For each of the 3 suggestions, provide: "
        "1. Genre & Trope Name (e.g., Cozy Paranormal Mystery, Reject Werewolf Romance, Sci-Fi Age-Gap Romance) "
        "2. The Target Audience & Why they are underserved "
        "3. A unique hook or concept that a new author could immediately write to dominate this niche. "
        "Output the entire report in English, but add a brief Japanese executive summary at the very beginning for the director."
    )

    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            save_workspace("01_market_report.md", result)
            print("✅ Global market research report generated successfully.")
        else:
            write_demo_report()
    except Exception as e:
        print(f"Error during research API call: {e}")
        write_demo_report()

def save_workspace(filename, content):
    os.makedirs("kdp_novels/workspace", exist_ok=True)
    with open(f"kdp_novels/workspace/{filename}", "w", encoding="utf-8") as f:
        f.write(content)

def write_demo_report():
    demo = """# 📊 Global Underserved Niche Research Report
## 日本語エグゼクティブサマリー
英語圏のAmazon.comにおいて、現在「BookTok」等で爆発的な需要があるにもかかわらず、既存の作品数が追いついていない3つの超ニッチジャンルを特定しました。
今回は、最もKindle Unlimitedで爆発しやすい 'Reject Werewolf Romance with a Second Chance'（拒絶された人狼ロマンスと二度目のチャンス） に焦点を絞り、オリジナルの作品を展開します。

## 1. Chosen Genre: Paranormal Romance (Werewolf/Shifter)
- **Trope:** Rejected Mate & Second Chance.
- **Why underserved:** Readers crave intense emotional angst where the female lead is rejected by her fated Alpha mate but returns stronger, finding a second-chance bond that drives the original rejector mad with jealousy.
"""
    save_workspace("01_market_report.md", demo)

if __name__ == "__main__":
    run_research()
