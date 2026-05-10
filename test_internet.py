import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

print("KEY USED:", os.getenv("GROQ_API_KEY"))  # <-- IMPORTANT

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": "Hello"}]
    )
    print(res.choices[0].message.content)
except Exception as e:
    print("ERROR:", e)
