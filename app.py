from flask import Flask, render_template
from crawler import get_metal_prices
from news import get_news
from datetime import datetime
import csv

app = Flask(__name__)

def get_trend(change_value):
    if change_value is None:
        return "same"
    if change_value > 0:
        return "up"
    elif change_value < 0:
        return "down"
    return "same"

def load_history():
    dates = []
    copper_history = []
    aluminum_history = []
    silver_history = []

    try:
        with open("data.csv", "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dates.append(row["date"])
                copper_history.append(float(row["copper"]))
                aluminum_history.append(float(row["aluminum"]))
                silver_history.append(float(row["silver"]))
    except Exception as e:
        print("读取历史数据失败：", e)

    return dates, copper_history, aluminum_history, silver_history

@app.route("/")
def index():
    prices = get_metal_prices()
    today_date = datetime.now().strftime("%Y-%m-%d")

    prices["copper"]["trend"] = get_trend(prices["copper"]["change"])
    prices["aluminum"]["trend"] = get_trend(prices["aluminum"]["change"])
    prices["silver"]["trend"] = get_trend(prices["silver"]["change"])

    dates, copper_history, aluminum_history, silver_history = load_history()

    events = get_news()

    analysis = """
无
"""

    return render_template(
        "index.html",
        prices=prices,
        events=events,
        dates=dates,
        copper_history=copper_history,
        aluminum_history=aluminum_history,
        silver_history=silver_history,
        today_date=today_date,
        analysis=analysis
    )

if __name__ == "__main__":
    app.run(debug=True)
