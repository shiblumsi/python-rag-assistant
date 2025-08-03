import os
import httpx
from dotenv import load_dotenv

load_dotenv()

def ask_llm(context: str, question: str) -> str:
    prompt = f"""You are a helpful assistant.
Answer the question based on the context.

Context:
{context}

Question:
{question}
"""

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",  
    }

    body = {
        "model": "openai/gpt-3.5-turbo", 
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"
