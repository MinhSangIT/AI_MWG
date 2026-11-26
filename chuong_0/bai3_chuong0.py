import requests

url = "https://httpbin.org/get"

# Tham số gửi lên API
params = {"name": "Sang", "course": "Agentic AI"}

# Gửi GET request
response = requests.get(url, params=params)

# Kiểm tra status code
print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()

    print("Args:", data["args"])
else:
    print("Lỗi khi gọi API:", response.status_code)
