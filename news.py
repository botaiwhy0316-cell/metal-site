import feedparser

def get_news():
    feeds = [
        "https://www.chinanews.com.cn/rss/finance.xml",
        "https://www.chinanews.com.cn/rss/world.xml"
    ]

    keywords = [
        "铜", "铝", "金属",
        "美元", "美联储", "加息", "降息",
        "战争", "冲突", "中东",
        "原油", "能源",
        "房地产", "基建", "经济"
    ]

    results = []

    for url in feeds:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")

            # ⭐ 关键词筛选
            if any(k in title for k in keywords):
                results.append({
                    "title": title,
                    "link": link
                })

    return results[:8]


if __name__ == "__main__":
    news = get_news()

    print("筛选后新闻数量：", len(news))

    for item in news:
        print(item["title"])
        print(item["link"])
        print("-" * 30)