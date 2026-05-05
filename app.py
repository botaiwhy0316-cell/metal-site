from flask import Flask, render_template
from crawler import get_metal_prices
from db import init_db, save_price, get_history
from news import get_news
from datetime import datetime

app = Flask(__name__)
init_db()

def get_trend(change_value):
    if change_value is None:
        return "same"

    if change_value > 0:
        return "up"
    elif change_value < 0:
        return "down"
    else:
        return "same"

@app.route("/")
def index():
    prices = get_metal_prices()

    today_date = datetime.now().strftime("%Y-%m-%d")

    # 暂时数据库只保存铜价和铝价
    save_price(
        prices["copper"]["today"],
        prices["aluminum"]["today"]
    )

    history = get_history()
    dates = [row[0] for row in history]
    copper_history = [row[1] for row in history]
    aluminum_history = [row[2] for row in history]

    # 趋势判断
    prices["copper"]["trend"] = get_trend(prices["copper"]["change"])
    prices["aluminum"]["trend"] = get_trend(prices["aluminum"]["change"])
    prices["silver"]["trend"] = get_trend(prices["silver"]["change"])

    events = get_news()

    analysis = """
铜价下跌 -100：

1. 今日铜均价较上日下跌，说明节前市场成交偏弱。
2. 五一假期期间，现货市场交易活跃度下降。
3. 下游采购节奏放缓，短期需求支撑不足。

铝价下跌 -90：

1. 铝价同步走弱，反映有色金属整体承压。
2. 节假日前后库存和采购节奏变化，对价格形成影响。
3. 短期仍需关注假期后下游复工和补库情况。

银价：

1. 银价受贵金属避险情绪、美元走势和工业需求共同影响。
2. 若国际局势紧张，银价可能受到一定支撑。
3. 需结合黄金、美元指数及工业金属整体走势继续观察。
"""

    return render_template(
        "index.html",
        prices=prices,
        events=events,
        dates=dates,
        copper_history=copper_history,
        aluminum_history=aluminum_history,
        today_date=today_date,
        analysis=analysis
    )

if __name__ == "__main__":
    app.run(debug=True)