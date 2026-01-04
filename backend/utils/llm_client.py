from google import genai
import json


client = genai.Client(api_key="AIzaSyBdT2AlPc1PXlL-ZaLKWXEgtKsiEzdQ9TU")

def call_llm(prompt: str) -> dict:
    response = client.models.generate_content(
        model="models/gemini-pro-latest",
        contents=prompt
    )

    text = response.text.strip()
    return json.loads(text)


