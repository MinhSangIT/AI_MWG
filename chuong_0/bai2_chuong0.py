import json

# Đọc dữ liệu từ products.json
with open("products.json", "r", encoding="utf-8") as file:
    products = json.load(file)

# Danh sách sản phẩm thỏa điều kiện
cheap_products = []

# Lọc sản phẩm
for product in products:
    if product["con_hang"] == True and product["gia"] < 20000000:
        cheap_products.append(product)

# In tên sản phẩm
print("Các sản phẩm còn hàng và giá dưới 20 triệu:")

for product in cheap_products:
    print(product["ten"])

# Ghi kết quả ra cheap.json
with open("cheap.json", "w", encoding="utf-8") as file:
    json.dump(cheap_products, file, ensure_ascii=False, indent=4)

print("\nĐã lưu kết quả vào cheap.json")
