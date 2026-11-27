import json
from datetime import datetime

TON_KHO = {
    "tivi 55 inch": {"so_luong": 12, "gia_vnd": 14990000},
    "tủ lạnh 300 lít": {"so_luong": 0, "gia_vnd": 9490000},
    "máy giặt 9kg": {"so_luong": 5, "gia_vnd": 7290000},
}

DON_HANG = {
    "DH001": {"trang_thai": "đang giao", "ngay_du_kien": "2026-11-28"},
    "DH002": {"trang_thai": "đã giao", "ngay_du_kien": "2026-11-20"},
}

THU = [
    "Thứ Hai",
    "Thứ Ba",
    "Thứ Tư",
    "Thứ Năm",
    "Thứ Sáu",
    "Thứ Bảy",
    "Chủ Nhật",
]


def tra_ton_kho(ten_san_pham):
    key = ten_san_pham.strip().lower()
    if key not in TON_KHO:
        return json.dumps(
            {"loi": f"Không tìm thấy sản phẩm: {ten_san_pham}"},
            ensure_ascii=False,
        )
    return json.dumps(
        {"ten_san_pham": key, **TON_KHO[key]},
        ensure_ascii=False,
    )


def tra_don_hang(ma_don):
    key = ma_don.strip().upper()
    if key not in DON_HANG:
        return json.dumps(
            {"loi": f"Không tìm thấy đơn hàng: {ma_don}"},
            ensure_ascii=False,
        )
    return json.dumps(
        {"ma_don": key, **DON_HANG[key]},
        ensure_ascii=False,
    )


# def lay_ngay_hien_tai():
    bay_gio = datetime.now()
    return json.dumps(
        {"ngay": bay_gio.strftime("%Y-%m-%d"), "thu": THU[bay_gio.weekday()]},
        ensure_ascii=False,
    )

def lay_ngay_hien_tai(**kwargs):
    bay_gio = datetime.now()
    return json.dumps(
        {"ngay": bay_gio.strftime("%Y-%m-%d"), "thu": THU[bay_gio.weekday()]},
        ensure_ascii=False,
    )

def tinh_an_toan(items):
    ket_qua = []
    tong_tien = 0

    for item in items:
        ten_san_pham = item["ten_san_pham"].strip().lower()
        so_luong = item["so_luong"]

        if ten_san_pham not in TON_KHO:
            return json.dumps(
                {"loi": f"Không tìm thấy sản phẩm: {ten_san_pham}"},
                ensure_ascii=False,
            )

        san_pham = TON_KHO[ten_san_pham]
        don_gia = san_pham["gia_vnd"]

        thanh_tien = don_gia * so_luong
        tong_tien += thanh_tien

        ket_qua.append(
            {
                "ten_san_pham": ten_san_pham,
                "so_luong": so_luong,
                "don_gia": don_gia,
                "thanh_tien": thanh_tien,
            }
        )

    return json.dumps(
        {
            "chi_tiet": ket_qua,
            "tong_tien": tong_tien,
        },
        ensure_ascii=False,
    )

HAM = {
    "tra_ton_kho": tra_ton_kho,
    "tra_don_hang": tra_don_hang,
    "lay_ngay_hien_tai": lay_ngay_hien_tai,
    "tinh_an_toan": tinh_an_toan
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "tra_ton_kho",
            "description": (
                "Tra số lượng tồn kho và giá (VND) của một sản phẩm theo tên. "
                "Dùng khi khách hỏi còn hàng không hoặc giá bao nhiêu."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ten_san_pham": {
                        "type": "string",
                        "description": "Tên sản phẩm, ví dụ: tivi 55 inch",
                    },
                },
                "required": ["ten_san_pham"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tra_don_hang",
            "description": (
                "Tra trạng thái và ngày giao dự kiến của một đơn hàng theo mã đơn. "
                "Dùng khi khách hỏi đơn hàng đang ở đâu."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ma_don": {
                        "type": "string",
                        "description": "Mã đơn hàng, ví dụ: DH001",
                    },
                },
                "required": ["ma_don"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lay_ngay_hien_tai",
            "description": (
                "Lấy ngày hôm nay và thứ trong tuần. "
                "Dùng khi cần biết hôm nay là ngày nào, thứ mấy."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
    },
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "tinh_an_toan",
    #         "description": (
    #             "tính số tiền cần thanh toán khi khách hỏi nhiều sản phẩm, liệt kê tổng từng loại rồi tính tổng pgair thanh toán"
    #         ),
    #         "parameters": {"type": "object", "properties": {}},
    #     },
    # },
    {
        "type": "function",
        "function": {
            "name": "tinh_an_toan",
            "description": (
                "lấy số lượng và tên sản phẩm"
                "Dùng khi mua nhiều sản phẩm khách hỏi tổng bao nhiêu tiền?.(liệt kê tổng từng sản phẩm trước khi trả thành tiền)"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "description": "Danh sách sản phẩm khách muốn mua",
                        "items": {
                            "type": "object",
                            "properties": {
                                "ten_san_pham": {
                                    "type": "string",
                                    "description": "Tên sản phẩm",
                                },
                                "so_luong": {
                                    "type": "integer",
                                    "description": "Số lượng sản phẩm",
                                },
                            },
                            "required": [
                                "ten_san_pham",
                                "so_luong",
                            ],
                        },
                    },
                },
                "required": ["items"],
            },
        },
    },
]
