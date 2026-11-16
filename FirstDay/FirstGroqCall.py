import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

print("Groq client initialized successfully!")


response = client.chat.completions.create(

    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": "You are a Good instructor."
        },
        {
            "role": "user",
            "content": "Expalin LLM."
        }
    ]
)

print(response.choices[0].message.content)
