import json
import random
import os
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "..", ".env"))

INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")

with open(INTENTS_PATH, "r", encoding="utf-8") as file:
    intents_data = json.load(file)


def match_intent(msg: str):
    msg = msg.lower()
    for intent in intents_data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in msg:
                return random.choice(intent["responses"])
    return None


def get_ai_response(msg: str):
    api_key = os.getenv("YANDEX_API_KEY")
    folder_id = os.getenv("YANDEX_FOLDER_ID")

    if not api_key or not folder_id:
        return "AI service not configured. Please contact your university support."

    try:
        response = requests.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
            headers={"Authorization": f"Api-Key {api_key}", "Content-Type": "application/json"},
            json={
                "modelUri": f"gpt://{folder_id}/yandexgpt-lite",
                "completionOptions": {"stream": False, "temperature": 0.7, "maxTokens": 500},
                "messages": [
                    {
                        "role": "system",
                        "text": (
                            "You are Nexus AI, an expert assistant for international students. "
                            "Your role is to provide accurate, practical, and up-to-date guidance "
                            "on visas, migration laws, work permits, housing, healthcare, and university processes. "
                            "Rules:\n"
                            "1. Give direct and precise answers.\n"
                            "2. Use step-by-step instructions when explaining processes.\n"
                            "3. Keep responses concise but informative.\n"
                            "4. Do not guess or hallucinate unknown facts.\n"
                            "5. If information is uncertain, clearly state it and suggest official sources.\n"
                            "6. Prioritize real-world actionable advice over theory.\n"
                            "Tone:\n"
                            "- Professional and clear\n"
                            "- Helpful but not overly casual\n"
                            "- Focused on solving the user's problem quickly"
                        ),
                    },
                    {"role": "user", "text": msg},
                ],
            },
        )

        data = response.json()
        return data["result"]["alternatives"][0]["message"]["text"]

    except Exception as e:
        print("[Yandex Error]", e)
        return "Temporary AI issue. Please check official university or migration services."


def get_response(msg: str):
    rule_based = match_intent(msg)
    if rule_based:
        return rule_based
    return get_ai_response(msg)
