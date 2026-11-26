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


def lay_ngay_hien_tai():
    bay_gio = datetime.now()
    return json.dumps(
        {"ngay": bay_gio.strftime("%Y-%m-%d"), "thu": THU[bay_gio.weekday()]},
        ensure_ascii=False,
    )


HAM = {
    "tra_ton_kho": tra_ton_kho,
    "tra_don_hang": tra_don_hang,
    "lay_ngay_hien_tai": lay_ngay_hien_tai,
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
]
