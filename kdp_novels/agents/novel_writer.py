import os
import requests

def run_writer():
    print("✍️ [KDP Writing Dept] Writing Chapter 1 in English with auto-editing/debugging...")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    blueprint_path = "kdp_novels/workspace/02_plot_blueprint.md"
    blueprint_context = ""
    if os.path.exists(blueprint_path):
        with open(blueprint_path, "r", encoding="utf-8") as f:
            blueprint_context = f.read()

    if not api_key:
        print("⚠️ API Key not found. Generating default English chapter...")
        write_demo_manuscript()
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
Using the following character profiles, chosen ending, and Save the Cat storyline blueprint:
{blueprint_context}

Write "Chapter 1" of this novel in English. 
Ensure the writing style is highly immersive, filled with deep sensory details, emotional tension, and compelling dialogue that matches the highest-selling US fiction on Amazon KDP.
After writing the chapter, perform an automatic self-review to correct any typos, grammatical errors, or plot inconsistencies, and output the polished, final version of Chapter 1.
"""

    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=90)
        if response.status_code == 200:
            result = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            with open("kdp_novels/workspace/03_novel_manuscript.md", "w", encoding="utf-8") as f:
                f.write(result)
            print("✅ Chapter 1 successfully written and edited in English.")
        else:
            write_demo_manuscript()
    except Exception as e:
        print(f"Error during writing API call: {e}")
        write_demo_manuscript()

def write_demo_manuscript():
    demo = """# 📚 Novel Manuscript: Elena's Rebirth
## Chapter 1: The Cold Rain of Silver Creek
The rain of Silver Creek always tasted like old metal. 
Elena pulled her tattered cloak tighter around her shoulders, keeping her gaze locked firmly on the muddy path. She could hear the howling of the pack in the distance—the annual Blue Moon Festival had begun, but she was not invited. She was the pack's ghost.
"""
    with open("kdp_novels/workspace/03_novel_manuscript.md", "w", encoding="utf-8") as f:
        f.write(demo)

if __name__ == "__main__":
    run_writer()
