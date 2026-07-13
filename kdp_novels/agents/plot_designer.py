import os
import requests

def run_plot_design():
    print("📐 [KDP Plot Design Dept] Generating global character profile and Save the Cat outline...")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    report_path = "kdp_novels/workspace/01_market_report.md"
    market_context = ""
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            market_context = f.read()

    if not api_key:
        print("⚠️ API Key not found. Generating default global blueprint...")
        write_demo_blueprint()
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
Based on the following global market research report:
{market_context}

Design a completely original, highly addictive fiction project targeting the Amazon.com US market. Do NOT copy any existing examples.
Generate a comprehensive blueprint containing:
1. **The Ultimate Ending (10 variants):** Brainstorm 10 different, highly satisfying or mind-blowing endings tailored to this niche. Then, select the most powerful, emotional, or plot-twist ending and explain how it will be fully executed.
2. **Character Profiles:** Create detailed profiles for the main characters (including physical appearance, inner flaws, desires, and secrets). Ensure they perfectly appeal to the target readers.
3. **Save the Cat! 15-Beat Storyline:** Create a detailed 15-beat outline of the novel, broken down by chapter. Every beat must build maximum emotional tension and hook the reader to turn the next page.

The entire output must be in English.
"""

    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            with open("kdp_novels/workspace/02_plot_blueprint.md", "w", encoding="utf-8") as f:
                f.write(result)
            print("✅ Global blueprint and Save the Cat outline successfully generated.")
        else:
            write_demo_blueprint()
    except Exception as e:
        print(f"Error during plot design API call: {e}")
        write_demo_blueprint()

def write_demo_blueprint():
    demo = """# 📐 Global Novel Blueprint & Character Profile
## Selected Niche: Rejected Mate Werewolf Romance
## Chosen Ending: 'The Alpha's Regret' (Intense emotional payoff/Second chance romance)
## Major Characters:
- **Elena Vance (19):** Slender, emerald eyes, silver-streaked dark hair. Hidden ancient bloodline. Fierce but deeply scarred by her pack's betrayal.
- **Alpha Nicholas (27):** Domineering, ruggedly handsome, eyes like molten gold. Cold and ruthless, but secretly harboring extreme regret.
## Save the Cat 15-Beat Outline:
- Chapter 1: The Opening Image (Elena's suffering) & Theme Stated...
"""
    with open("kdp_novels/workspace/02_plot_blueprint.md", "w", encoding="utf-8") as f:
        f.write(demo)

if __name__ == "__main__":
    run_plot_design()
