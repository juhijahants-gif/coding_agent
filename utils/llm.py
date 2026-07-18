import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt: str, model="llama-3.1-8b-instant") -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ⚡ use fast + stable first
            messages=[
                {"role": "system", "content": "You are an expert coding assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )

        # ✅ SAFE EXTRACTION
        if response and response.choices:
            message = response.choices[0].message

            if message and message.content:
                return message.content.strip()

        return None  # 👈 important

    except Exception as e:
        print("LLM ERROR:", e)
        return None