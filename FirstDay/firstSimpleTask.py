
# Install packages in terminal:
# pip install openai python-dotenv

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Initialize Gemini client using OpenAI SDK
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
print("Client initialized:", client)
# Send request
response = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=[
        {
            {"role": "system", "content": "You are a witty travel guide."},
            {"role": "user",   "content": "Suggest one thing to do in Bangalore."},
        }
    ]
)

# Print response
print(response.choices[0].message.content)
