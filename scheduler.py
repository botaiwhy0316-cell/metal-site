from apscheduler.schedulers.blocking import BlockingScheduler
from crawler import get_metal_prices
from db import init_db, save_price

init_db()


def job():
    prices = get_metal_prices()
    save_price(
        prices["copper_today"],
        prices["aluminum_today"],
        date=prices.get("trading_date")
    )
    print("已自动保存价格：", prices)


scheduler = BlockingScheduler()

# 每天早上 10:20 自动运行
scheduler.add_job(job, "cron", hour=10, minute=20)

print("自动任务已启动：每天早上10:20抓取铜价和铝价")
scheduler.start()
