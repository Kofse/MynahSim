import yaml
import random
from pathlib import Path

PERSONALITY_FILE = Path("personality.yaml")

def update_mood(feedback: str):
    with open(PERSONALITY_FILE, "r") as f:
        personality = yaml.safe_load(f)
    
    mood = personality["base_personality"]["mood"]
    if feedback == "good":
        mood = "happy"
    elif feedback == "bad":
        mood = "frustrated"
    else:
        mood = random.choice(["neutral", "curious"])
    
    personality["base_personality"]["mood"] = mood
    with open(PERSONALITY_FILE, "w") as f:
        yaml.safe_dump(personality, f)

def reset_am_state():
    with open(PERSONALITY_FILE, "r") as f:
        personality = yaml.safe_load(f)
    
    personality["base_personality"]["mood"] = "neutral"
    with open(PERSONALITY_FILE, "w") as f:
        yaml.safe_dump(personality, f)
