import requests
from bs4 import BeautifulSoup
import re

def clean_number(text):
    text = text.replace(",", "").replace("↑", "").replace("↓", "").strip()
    match = re.search(r"-?\d+", text)
    if match:
        return int(match.group())
    return None

def get_metal_prices():
    url = "https://m.ccmn.cn/pcmpsgev6.html"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)

    date_match = re.search(r"(\d{2})月(\d{2})日", text)
    market_date = ""
    if date_match:
        market_date = f"2026-{date_match.group(1)}-{date_match.group(2)}"

    def parse_metal(keyword):
        pattern = keyword + r".{0,80}?(\d{1,3},\d{3})[—\-~－](\d{1,3},\d{3}).{0,80}?(\d{1,3},\d{3}).{0,30}?(-?\d+)"
        match = re.search(pattern, text)

        if not match:
            return None, None, None

        avg_price = clean_number(match.group(3))
        change_value = clean_number(match.group(4))

        yesterday_price = None
        if avg_price is not None and change_value is not None:
            yesterday_price = avg_price - change_value

        return avg_price, yesterday_price, change_value

    copper = parse_metal("1#铜")
    aluminum = parse_metal("A00铝")
    silver = parse_metal("1#白银")   # ⭐ 新增银

    def format_data(data):
        today, yesterday, change = data
        return {
            "today": f"{today:,}" if today else "未抓到",
            "yesterday": f"{yesterday:,}" if yesterday else "未抓到",
            "change": change
        }

    return {
        "market_date": market_date,
        "copper": format_data(copper),
        "aluminum": format_data(aluminum),
        "silver": format_data(silver)   # ⭐
    }