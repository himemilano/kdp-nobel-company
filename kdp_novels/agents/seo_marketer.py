import os
import requests

def run_marketing():
    print("💰 [KDP Marketing Dept] Generating global SEO metadata & English book description...")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    manuscript_path = "kdp_novels/workspace/03_novel_manuscript.md"
    manuscript_context = ""
    if os.path.exists(manuscript_path):
        with open(manuscript_path, "r", encoding="utf-8") as f:
            manuscript_context = f.read()

    if not api_key:
        print("⚠️ API Key not found. Generating default SEO description...")
        write_demo_seo()
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
Create a highly optimized book title, subtitle, and an extremely compelling book description in English for the Amazon.com (US KDP store) based on the following novel manuscript:
{manuscript_context}

Your output must strictly follow the 3-part blueprint of top-selling werewolf/romance books on Amazon:
1) **The Hook (First lines):** Choose the most dramatic, emotional, or sensory-heavy scene from the book to capture the reader's attention instantly. Use short, punchy paragraphs.
2) **The Description:** Describe the plot in a way that creates extreme tension, emphasizing the tropes (e.g., Rejected Mate, Secret Identity, Second Chance, Ruthless Alpha) to trigger the reader's emotional buying impulse.
3) **Niche & Keywords list:** Add a clean list of highly searched tropes/keywords at the end (e.g., ✔️ Rejected Mate, ✔️ Age Gap, ✔️ Alpha Romance) to dominate KDP search rankings.
"""

    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            with open("kdp_novels/workspace/04_kdp_seo_meta.md", "w", encoding="utf-8") as f:
                f.write(result)
            print("✅ Amazon US KDP SEO title and book description successfully generated.")
        else:
            write_demo_seo()
    except Exception as e:
        print(f"Error during marketing API call: {e}")
        write_demo_seo()

def write_demo_seo():
    demo = """# 💰 Amazon US KDP SEO Metadata
## Book Title Option
"The Alpha's Regret: A Rejected Mate Romance (Silver Creek Shifters Book 1)"

## Compelling Book Description (HTML ready for KDP)
"Elena, you are nothing but a weak, mateless omega. I reject you."

With those words, Alpha Nicholas shattered Elena's world, leaving her to die in the freezing rain. But he didn't know one thing... she was carrying a secret that would rewrite the laws of the wolf packs forever.

Three years later, Elena returns—no longer weak, and definitely no longer his. But Nicholas is now desperate to claim her. Will he survive her vengeance?

### What's inside this book:
- ✔️ Rejected Mate Romance
- ✔️ Second Chance Bond
- ✔️ Domineering Alpha & Secret Bloodline
- ✔️ Page-turning Emotional Angst
"""
    with open("kdp_novels/workspace/04_kdp_seo_meta.md", "w", encoding="utf-8") as f:
        f.write(demo)

if __name__ == "__main__":
    run_marketing()
