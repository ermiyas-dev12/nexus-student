import json
import random
import os
from groq import Groq

# ---------- LOAD INTENTS ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")

with open(INTENTS_PATH, "r", encoding="utf-8") as file:
    intents_data = json.load(file)

# ---------- GROQ CLIENT ----------
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

# ---------- RULE-BASED MATCH ----------
def match_intent(msg: str):
    msg = msg.lower()
    for intent in intents_data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in msg:
                return random.choice(intent["responses"])
    return None

# ---------- AI FALLBACK ----------
def get_ai_response(msg: str):
    if not client:
        return "AI service not configured. Please contact your university support."
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant helping international students in Russia. "
                        "Provide short, accurate, and practical answers about visa, work, housing, and healthcare."
                    )
                },
                {"role": "user", "content": msg}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Groq Error] {e}")
        return "Temporary AI issue. Please check official university or migration services."

# ---------- MAIN ----------
def get_response(msg: str):
    rule_based = match_intent(msg)
    if rule_based:
        return rule_based
    return get_ai_response(msg)
