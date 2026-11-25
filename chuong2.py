from common import ask

# region

# SYSTEM = """Bạn là bot trích xuất dữ liệu. Chỉ trả về JSON hợp lệ, không thêm
# chữ nào khác.
# ### Chỉ dẫn
# Trả về JSON với đúng các khóa sau:
# - ten (chuỗi)
# - dia_chi (chuỗi)
# - so_dien_thoai (chuỗi)
# - tren_18+ (yes/no)
# ### Ngữ cảnh
# Địa chỉ thường đứng sau cụm 'Giao đến' hoặc 'Địa chỉ'. Số điện thoại gồm 10
# chữ số.
# ### Ví dụ đầu ra
# {"ten": "Nguyễn Văn A", "dia_chi": "12 Lê Lợi, Quận 1, TP.HCM",
# "so_dien_thoai": "0901234567"}"""
# tin_nhan = "Chào shop, mình đặt 1 laptop. Giao đến: Trần Thị B, 45 Nguyễn Trãi, Quận 5, TP.HCM. SĐT 0987654321. 16t. Cảm ơn!"
# resp = ask(
#     [{"role": "system", "content": SYSTEM}, {"role": "user", "content": tin_nhan}],
#     temperature=0,
#     max_completion_tokens=1000,
# )
# print(resp.choices[0].message.content)

# endregion

# region
# SYSTEM = """Bạn là nhân viên tư vấn của một cửa hàng điện máy.
# Trả lời ngắn gọn, thân thiện. Mỗi lần chỉ hỏi tối đa một câu.
# Nếu không biết, hãy nói không biết, đừng đoán."""
# messages = [
#     {"role": "system", "content": SYSTEM},
#     {"role": "user", "content": "Mình cần mua tivi."},
#     {
#         "role": "assistant",
#         "content": "Bạn định đặt tivi ở phòng nào và cóngân sách khoảng bao nhiêu?",
#     },
#     {"role": "user", "content": "Phòng khách, khoảng 15 triệu."},
# ]
# resp = ask(messages, max_completion_tokens=1000)
# print(resp.choices[0].message.content)

# endregion

# region

# SYSTEM = "Phân loại tin nhắn của khách vào đúng một nhãn: tu_van, bao_hanh, khieu_nai, khac. Chỉ trả về nhãn, không giải thích."
# vi_du = [
#     ("Laptop nào hợp cho sinh viên?", "tu_van"),
#     ("Tivi mình mua tháng trước bị sọc màn hình.", "bao_hanh"),
#     ("Nhân viên giao hàng thái độ rất tệ.", "khieu_nai"),
# ]


# def phan_loai(tin):
#     messages = [{"role": "system", "content": SYSTEM}]

#     for hoi, nhan in vi_du:
#         messages.append({"role": "user", "content": hoi})
#         messages.append({"role": "assistant", "content": nhan})
#     messages.append({"role": "user", "content": tin})
#     resp = ask(messages, temperature=0, max_completion_tokens=500)
#     return resp.choices[0].message.content.strip()


# print(phan_loai("Máy giặt của mình kêu to quá, còn bảo hành không?"))

# endregion

# region

# resp = ask(
#     [
#         {
#             "role": "user",
#             "content": "Tóm tắt khái niệm API trong 2 câu. Kết thúc bằng",
#         }
#     ],
#     stop=["###"],
#     max_completion_tokens=1000,
#     temperature=0.3,
# )
# print(resp.choices[0].message.content)  # chuỗi ### không xuất hiện trong kết quả

# endregion

# region strict

# import json
# schema = {
#     'type': 'object',
#     'properties': {
#     'loai_san_pham': {'type': 'string'},
#     'ngan_sach_vnd': {'type': ['integer', 'null']},
#     'nhu_cau': {'type': 'string'},
#     'muc_do_gap': {'type': 'string', 'enum': ['thap', 'trung_binh','cao']},
# },
# 'required': ['loai_san_pham', 'ngan_sach_vnd', 'nhu_cau', 'muc_do_gap'],
# 'additionalProperties': False,
# }
# SYSTEM = '''Trích xuất yêu cầu mua hàng của khách.
# Nếu không có thông tin ngân sách thì dùng null.
# Nếu tin nhắn không liên quan đến mua hàng thì loai_san_pham là chuỗi rỗng.'''
# resp = ask(
# [
# {'role': 'system', 'content': SYSTEM},
# {'role': 'user', 'content': 'Mình cần mua tivi cho phòng khách, tầm 15 triệu, tuần này cần gấp.'},
# ],
# response_format={
# 'type': 'json_schema',
# 'json_schema': {'name': 'yeu_cau_khach', 'strict': False, 'schema':
# schema},
# },
# max_completion_tokens=1500,
# )
# data = json.loads(resp.choices[0].message.content)
# print(data)

# endregion

# region Pydantic, kiểm tra và thử lại (chế độ best-effort)
# import json
# from typing import Optional, Literal
# from pydantic import BaseModel, ValidationError
# from groq import BadRequestError
# from common import ask


# class YeuCauKhach(BaseModel):
#     loai_san_pham: str
#     ngan_sach_vnd: Optional[int] = None
#     nhu_cau: str
#     muc_do_gap: Literal["thap", "trung_binh", "cao"]


# SYSTEM = """Trích xuất yêu cầu mua hàng của khách.
# Nếu không có thông tin ngân sách thì để null.
# Nếu tin nhắn không liên quan đến mua hàng thì loai_san_pham là chuỗi rỗng."""


# def trich_xuat(tin, so_lan_thu=3):
#     for lan in range(so_lan_thu):
#         try:
#             resp = ask(
#                 [
#                     {"role": "system", "content": SYSTEM},
#                     {"role": "user", "content": tin},
#                 ],
#                 response_format={
#                     "type": "json_schema",
#                     "json_schema": {
#                         "name": "yeu_cau_khach",
#                         "schema": YeuCauKhach.model_json_schema(),
#                     },
#                 },
#                 max_completion_tokens=1500,
#             )
#             return YeuCauKhach.model_validate(json.loads(resp.choices[0].message.content))
#         except (ValidationError, json.JSONDecodeError, BadRequestError) as loi:
#             print(f"Lần {lan + 1} thất bại:", loi)
#     return None  # chuyển cho người xửlý


# print(trich_xuat("Mình muốn mua , ngân sách 10 triệu."))

# endregion

TIN_MAU = [
    "Mình cần mua tivi 55 inch cho phòng khách, khoảng 15 triệu, cần gấp trong tuần này.",
    "Tủ lạnh nhà mình đang bị chảy nước, còn bảo hành không shop?",
    "Máy giặt giao trễ 3 ngày mà không ai báo, mình rất bực.",
    "Hôm nay trời đẹp quá nhỉ!",
    "Cho mình hỏi laptop cho dân thiết kế đồ họa, ngân sách thoải mái.",
    "minh muốn mua bánh xe",
    "Tủ lạnh mình mới mua bị ồn, shop tư vấn giúp mình nên đổi hay sửa?"
]

# region bai 1


# TIN_GIAO_HANG = """
# Mình muốn đặt hàng một chiếc bàn làm việc.
# Giao hàng đến 25 Nguyễn Huệ, phường Bến Nghé,
# Quận 1, TP.HCM.
# Người nhận là Nguyễn Văn An, số điện thoại 0901234567.
# """

# PROMPT_SO_SAI = "Lấy địa chỉ giao hàng."

# PROMPT_DAY_DU = """
# Bạn là nhân viên xử lý đơn hàng của một cửa hàng thương mại điện tử.

# Nhiệm vụ:
# Trích xuất thông tin địa chỉ giao hàng từ tin nhắn khách hàng.

# Ngữ cảnh:
# Tin nhắn có thể chứa thông tin sản phẩm, địa chỉ,
# người nhận và số điện thoại.

# Định dạng đầu ra:
# Chỉ trả về JSON hợp lệ với cấu trúc:
# {
#     "dia_chi_giao_hang": "string hoặc null"
# }

# Ràng buộc:
# - Chỉ lấy địa chỉ được khách hàng cung cấp.
# - Không tự suy đoán hoặc bổ sung thông tin.
# - Nếu không có địa chỉ giao hàng, trả về null.
# - Không giải thích, không thêm chữ ngoài JSON.
# """

# from common import ask

# for i in range(3):
#     resp = ask(
#         [
#             # {"role": "system", "content": PROMPT_SO_SAI},
#             {"role": "system", "content": PROMPT_DAY_DU},
#             {"role": "user", "content": TIN_GIAO_HANG},
#         ],
#         temperature=0,
#         max_completion_tokens=500,
#     )

#     print(f"Lần {i + 1}:")
#     print(resp.choices[0].message.content)

# endregion

# region bai 2
from common import ask

SYSTEM = """
Phân loại tin nhắn của khách vào đúng một nhãn:
tu_van, bao_hanh, khieu_nai, khac.
Chỉ trả về nhãn, không giải thích.
"""

vi_du = [
    ("Laptop nào hợp cho sinh viên?", "tu_van"),
    ("Tivi mình mua tháng trước bị sọc màn hình.", "bao_hanh"),
    ("Nhân viên giao hàng thái độ rất tệ.", "khieu_nai"),
]

vi_du_moi = vi_du + [
    (
        "Đơn hàng của tôi giao trễ nhiều ngày, không ai thông báo. Tôi rất không hài lòng.",
        "khieu_nai"
    )
]


def phan_loai(tin, examples=vi_du):

    messages = [{"role": "system", "content": SYSTEM}]

    for hoi, nhan in examples:
        messages.append({"role": "user", "content": hoi})
        messages.append({"role": "assistant", "content": nhan})

    messages.append({"role": "user", "content": tin})

    resp = ask(messages, temperature=0, max_completion_tokens=500)

    return resp.choices[0].message.content.strip()


print("===== KẾT QUẢ TRƯỚC KHI THÊM FEW-SHOT =====")

# print(f"vi_du_moi: {vi_du_moi}")

ket_qua_truoc = []

for i, tin in enumerate(TIN_MAU, 1):
    # nhan = phan_loai(tin)
    nhan = phan_loai(tin, vi_du_moi)
    ket_qua_truoc.append(nhan)

    print(f"Tin {i}: {tin}")
    print(f"Nhãn: {nhan}")
    print("-" * 50)
# endregion

#region bai 2: b

# PROMPT_SLOGAN = """
# Bạn là chuyên gia sáng tạo nội dung quảng cáo.

# Hãy viết một slogan ngắn gọn, sáng tạo cho cửa hàng điện máy.
# Slogan cần thu hút khách hàng, dễ nhớ và thể hiện sự uy tín.
# Chỉ trả về một slogan, không giải thích.
# """


# def tao_slogan(temperature):
#     resp = ask(
#         [
#             {
#                 "role": "system",
#                 "content": "Bạn là chuyên gia marketing."
#             },
#             {
#                 "role": "user",
#                 "content": PROMPT_SLOGAN
#             }
#         ],
#         temperature=temperature,
#         max_completion_tokens=200
#     )

#     print("Slogan:", resp.choices[0].message.content)
#     print("Usage:", resp.usage)


# print("===== TEMPERATURE 0.2 =====")

# for i in range(3):
#     print(f"\nLần {i + 1}")
#     tao_slogan(0.2)


# print("\n===== TEMPERATURE 0.9 =====")

# for i in range(3):
#     print(f"\nLần {i + 1}")
#     tao_slogan(0.9)
# endregion

#region bai3: Structured output
# import json
# from typing import Optional, Literal

# from pydantic import BaseModel, ValidationError
# from groq import BadRequestError

# from common import ask


# class YeuCauKhach(BaseModel):
#     loai_san_pham: str
#     ngan_sach_vnd: Optional[int] = None
#     nhu_cau: str
#     muc_do_gap: Literal["thap", "trung_binh", "cao"]

# SYSTEM_TRICH_XUAT = """
# Bạn là hệ thống trích xuất thông tin mua hàng của khách hàng.

# Nhiệm vụ:
# Trích xuất 4 thông tin:
# - loai_san_pham
# - ngan_sach_vnd
# - nhu_cau
# - muc_do_gap

# Quy tắc:
# 1. Nếu không có thông tin ngân sách thì trả về null.
# 2. Chuyển ngân sách sang đơn vị VND.
#    Ví dụ: 15 triệu = 15000000.
# 3. Nếu khách không nói rõ nhu cầu thì mô tả ngắn gọn
#    dựa trên nội dung tin nhắn.
# 4. Mức độ gấp:
#    - thap: Không có yêu cầu gấp.
#    - trung_binh: Có nhu cầu mua nhưng không quá gấp.
#    - cao: Khách cần gấp hoặc có thời hạn cụ thể.
# 5. Nếu tin nhắn không có lấy dc dữ liệu
#    - loai_san_pham là chuỗi rỗng.
#    - ngan_sach_vnd là null.
#    - nhu_cau là chuỗi rỗng.
#    - muc_do_gap là thap.
# 6. loai_san_pham chỉ gồm thiết bị điện tử. còn lại trả khác. null nếu k không nói về sp
# """

# def trich_xuat(tin, so_lan_thu=3):

#     for lan in range(so_lan_thu):

#         try:
#             resp = ask(
#                 [
#                     {
#                         "role": "system",
#                         "content": SYSTEM_TRICH_XUAT
#                     },
#                     {
#                         "role": "user",
#                         "content": tin
#                     }
#                 ],

#                 response_format={
#                     "type": "json_schema",
#                     "json_schema": {
#                         "name": "yeu_cau_khach",
#                         "schema": YeuCauKhach.model_json_schema()
#                     }
#                 },

#                 max_completion_tokens=1500
#             )

#             content = resp.choices[0].message.content

#             data = json.loads(content)

#             return YeuCauKhach.model_validate(data)

#         except (
#             ValidationError,
#             json.JSONDecodeError,
#             BadRequestError
#         ) as loi:

#             print(f"Lần {lan + 1} thất bại:", loi)

#     return None

# print("===== KẾT QUẢ STRUCTURED OUTPUT =====")

# ket_qua = []

# for i, tin in enumerate(TIN_MAU, 1):

#     result = trich_xuat(tin)

#     if result:
#         ket_qua.append({
#             "STT": i,
#             "Tin nhắn": tin,
#             "Sản phẩm": result.loai_san_pham,
#             "Ngân sách": result.ngan_sach_vnd,
#             "Nhu cầu": result.nhu_cau,
#             "Mức độ gấp": result.muc_do_gap
#         })

#     else:
#         ket_qua.append({
#             "STT": i,
#             "Tin nhắn": tin,
#             "Sản phẩm": "Lỗi",
#             "Ngân sách": None,
#             "Nhu cầu": "Không trích xuất được",
#             "Mức độ gấp": "Không xác định"
#         })


# # In bảng kết quả
# print("\n===== BẢNG KẾT QUẢ =====")

# for row in ket_qua:
#     print("-" * 100)

#     for key, value in row.items():
#         print(f"{key}: {value}")

#endregion