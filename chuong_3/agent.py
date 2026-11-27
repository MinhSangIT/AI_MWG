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
        ket_qua = HAM[ten](**tham_so)  # run func
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
        print(buoc)

        resp = ask(
            messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.3,
            max_completion_tokens=1500,
        )
        tin = resp.choices[0].message
        if buoc == 2:
            print(messages)
        # print(tin)
        print(tin.tool_calls)

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
    print(tro_ly("Mua 2 tivi 55 inch và 1 máy giặt 9kg thì tổng bao nhiêu tiền?"))

    # cau_hoi = [
    #     'Hôm nay là thứ mấy?'
    # ]

    # for i, cau in enumerate(cau_hoi, start=1):
    #     print(f'\n========== CÂU {i} ==========')
    #     print('Người dùng:', cau)
    #     ket_qua = tro_ly(cau)
    #     print('Trợ lý:', ket_qua)
