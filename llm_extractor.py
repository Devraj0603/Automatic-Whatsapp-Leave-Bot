import google.generativeai as genai
import json

genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")


def extract_leave(message):

    prompt = f"""
Extract leave details.

Return ONLY JSON.

Format:
{{
    "employee": "",
    "leave_type": "",
    "days": 1,
    "reason": ""
}}

Message:
{message}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return json.loads(text)
