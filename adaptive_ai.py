import os
import json
import yaml
import threading
import time
from pathlib import Path
from gpt4all import GPT4All
from web_tools import duckduckgo_search, scrape_website, clean_old_cache
from memory import Memory
from emotion import update_mood, reset_am_state

# Config paths
PERSONALITY_FILE = Path("personality.yaml")
HISTORY_DIR = Path("interaction_history")
MODEL_NAME = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
MODEL_PATH = Path("models") / MODEL_NAME

# Load personality
with open(PERSONALITY_FILE, "r") as f:
    personality = yaml.safe_load(f)

# Initialize memory
memory = Memory()

def log_interaction(user_input: str, ai_response: str):
    today = time.strftime("%Y-%m-%d")
    log_file = HISTORY_DIR / f"{today}.log"
    with open(log_file, "a") as f:
        f.write(json.dumps({"user": user_input, "ai": ai_response}) + "\n")

def generate_response(user_input: str) -> str:
    # Web search
    if "search for" in user_input.lower():
        query = user_input.split("search for")[-1].strip()
        results = duckduckgo_search(query)
        return "\n".join([f"{r['title']}\n{r['link']}" for r in results[:3]])
    
    # Fact checking
    if "fact check" in user_input.lower():
        query = user_input.split("fact check")[-1].strip()
        results = duckduckgo_search(query)
        claims = []
        for result in results[:3]:
            content = scrape_website(result["link"])
            if "yes" in content.lower() or "true" in content.lower():
                claims.append(f"{result['title']}: Likely true")
            elif "no" in content.lower() or "false" in content.lower():
                claims.append(f"{result['title']}: Likely false")
            else:
                claims.append(f"{result['title']}: Uncertain")
        return "\n".join(claims)
    
    # Generate response
    prompt = f"""
    [System]
    You are an AI assistant. Current mood: {personality['base_personality']['mood']}
    [User] {user_input}
    [Response]
    """
    model = GPT4All(MODEL_NAME, model_path="models")
    response = model.generate(prompt, max_tokens=300)
    return response.strip()

def periodic_cleanup():
    while True:
        time.sleep(24 * 3600)  # 24 hours
        clean_old_cache()

def main():
    # Initial cleanup
    clean_old_cache()
    
    # Start cleanup thread
    threading.Thread(target=periodic_cleanup, daemon=True).start()
    
    print("AI Assistant Ready! Safeword: 'epsilon'")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "epsilon":
            reset_am_state()
            print("AI: Mood reset.")
            continue
        if user_input.lower() == "exit":
            break
        
        response = generate_response(user_input)
        print(f"AI: {response}")
        log_interaction(user_input, response)
        update_mood("neutral")  # Simplified feedback

if __name__ == "__main__":
    main()
