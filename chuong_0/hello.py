import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Giải thích LLM cho học sinh cấp 3 trong 3 câu",
        }
    ],
)

# In nội dung trả lời
print("AI:", response.choices[0].message.content)

# Thống kê token
print("\n--- TOKEN USAGE ---")
print("Token đầu vào:", response.usage.prompt_tokens)
print("Token đầu ra:", response.usage.completion_tokens)
print("Tổng token:", response.usage.total_tokens)
