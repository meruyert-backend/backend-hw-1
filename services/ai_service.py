from openai import OpenAI
import json

client = OpenAI(api_key="YOUR_API_KEY")


def extract_tasks(text: str):
    prompt = f"""
Extract tasks from the following client communication.

Return ONLY valid JSON in this format:
[
  {{
    "title": "task title",
    "deadline": "optional deadline or null"
  }}
]

Text:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        tasks = json.loads(content)
    except:
        tasks = []

    return tasks