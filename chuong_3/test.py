
from common import ask

SYSTEM = """Bạn là nhân viên tư vấn của cửa hàng điện máy.
Dùng công cụ để tra tồn kho, giá và đơn hàng, đừng đoán.
Nếu công cụ báo lỗi, hãy xin lỗi và hỏi lại khách để làm rõ.
Trả lời ngắn gọn bằng tiếng Việt.
{"ten_san_pham": "tivi 55 inch", "so_luong": 12, "gia_vnd": 14990000}
"DH002": {"trang_thai": "đã giao", "ngay_du_kien": "2026-11-20"},

"""


tin_nhan = "Tivi 55 inch còn hàng không và giá bao nhiêu?DH002"

resp = ask(
    [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": tin_nhan},
        
    ],
    temperature=0.9,
    max_completion_tokens=1000,
)
print(resp.choices[0].message.content)