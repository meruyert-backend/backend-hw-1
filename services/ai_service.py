from dotenv import load_dotenv
load_dotenv()

import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_tasks(text: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict JSON generator. "
                    "Extract tasks from text. "
                    "Return ONLY a JSON array. No explanations."
                )
            },
            {
                "role": "user",
                "content": f"""
Extract tasks from this text.

Rules:
- Return ONLY JSON
- No markdown
- No explanations
- If no tasks → return []

Format:
[
  {{
    "title": "task title",
    "deadline": null
  }}
]

Text:
{text}
"""
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    # 🔥 Clean defensive
    content = content.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(content)

        # ✅ Validate structure
        if not isinstance(parsed, list):
            print("AI ERROR: Not a list")
            return []

        clean_tasks = []
        for t in parsed:
            if isinstance(t, dict) and "title" in t:
                clean_tasks.append({
                    "title": t["title"],
                    "deadline": t.get("deadline")
                })

        print("AI TASKS:", clean_tasks)
        return clean_tasks

    except Exception:
        print("AI PARSE ERROR:", content)
        return []