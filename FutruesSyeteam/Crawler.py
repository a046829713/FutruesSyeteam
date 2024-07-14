import requests
import json


year = 2015

# 设置目标URL
url = f'https://www.yuantafutures.com.tw/api/TradeCal01?format=json&select02=%E6%9C%9F%E8%B2%A8&y={year}'


print("目前請求網址:",url)

# 创建请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 检查响应状态码
if response.status_code == 200:
    # 解析JSON数据
    data = response.json()
    print(json.dumps(data, indent=4, ensure_ascii=False))
else:
    print("Failed to retrieve data:", response.status_code)
