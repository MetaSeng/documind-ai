import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load environment variables from .env
load_dotenv()

# 2. Initialize Groq client
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# 3. Send a test request to the model
response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[{"role": "user", 
    "content": "Where is Cambodia?."}]
)

# 4. Print the generated response
print(response.choices[0].message.content)