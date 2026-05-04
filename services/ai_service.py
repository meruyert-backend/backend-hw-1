from dotenv import load_dotenv
load_dotenv()

import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_tasks(text: str):
    prompt = f"""
    Extract tasks from the following client communication.

    Return ONLY valid JSON list:
    [
      {{
        "title": "task title",
        "deadline": null
      }}
    ]

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    # 🔥 очистка
    content = content.replace("```json", "").replace("```", "").strip()

    try:
        tasks = json.loads(content)
        print("AI TASKS:", tasks)   # 👈 ДОБАВЬ ЭТО
        return tasks
    except Exception as e:
        print("AI PARSE ERROR:", content)
        return []