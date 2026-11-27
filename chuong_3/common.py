import time
from groq import Groq, RateLimitError

MODEL = "openai/gpt-oss-120b"  # đối chiếu trang Models của Groq
# qwen/qwen3.8-27b và các model Llama hỗ trợ goi nhieu tool cung luc
client = Groq()  # tự đọc GROQ_API_KEY từ biến môi trường

def ask(messages, **kwargs):
    for attempt in range(3):
        try:
            return client.chat.completions.create(
                model=MODEL, messages=messages, **kwargs
            )
        except RateLimitError:
            time.sleep(5 * (attempt + 1))  # chờ rồi thử lại
    raise RuntimeError("Vẫn bị giới hạn tốc độ sau 3 lần thử")
