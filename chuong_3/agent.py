import json

from common import ask
from tools_dien_may import HAM, TOOLS

SYSTEM = """Bạn là nhân viên tư vấn của cửa hàng điện máy.
Dùng công cụ để tra tồn kho, giá và đơn hàng, đừng đoán.
Nếu công cụ báo lỗi, hãy xin lỗi và hỏi lại khách để làm rõ.
Trả lời ngắn gọn bằng tiếng Việt."""


def chay_tool(tool_call):
    ten = tool_call.function.name
    try:
        if ten not in HAM:
            raise ValueError(f"Không có công cụ: {ten}")
        tham_so = json.loads(tool_call.function.arguments)
        ket_qua = HAM[ten](**tham_so)
    except Exception as loi:
        ket_qua = json.dumps({"loi": str(loi)}, ensure_ascii=False)
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": ten,
        "content": ket_qua,
    }


def tro_ly(cau_hoi, toi_da=6):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": cau_hoi},
    ]
    for buoc in range(toi_da):
        resp = ask(
            messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.3,
            max_completion_tokens=1500,
        )
        tin = resp.choices[0].message
        if not tin.tool_calls:
            return tin.content  # không cần công cụ nữa: đây là câu trả lời cuối
        messages.append(tin)  # giữ lại yêu cầu gọi công cụ của mô hình
        for tc in tin.tool_calls:
            print(
                f"  [bước {buoc + 1}] gọi {tc.function.name}({tc.function.arguments})"
            )
            messages.append(chay_tool(tc))  # chạy hàm rồi thêm kết quả vào hội thoại
    return "Xin lỗi, mình chưa xử lý xong yêu cầu này."


if __name__ == "__main__":
    print(tro_ly("Tivi 55 inch còn hàng không và giá bao nhiêu?"))
