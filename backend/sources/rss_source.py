import feedparser
from sources.base_source import MarketSource

RSS_FEEDS = [
    {
        "name": "CNBC Markets",
        "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    },
    {
        "name": "MarketWatch",
        "url": "https://feeds.content.dowjones.io/public/rss/mw_topstories",
    },
    {
        "name": "Investing.com",
        "url": "https://www.investing.com/rss/news.rss",
    },
]


class RSSSource(MarketSource):
    name = "RSS Financial Feeds"
    source_type = "RSS News"

    def fetch(self, ticker: str, limit: int = 10):
        items = []

        company_map = {
            "TSLA": ["tesla", "tsla", "elon", "robotaxi"],
            "NVDA": ["nvidia", "nvda", "gpu", "ai chip"],
            "AAPL": ["apple", "aapl", "iphone"],
            "MSFT": ["microsoft", "msft", "azure"],
            "AMZN": ["amazon", "amzn", "aws"],
            "META": ["meta", "facebook", "instagram"],
            "GOOGL": ["google", "alphabet", "googl"],
            "BTC": ["bitcoin", "btc"],
            "ETH": ["ethereum", "eth"],
            "SOL": ["solana", "sol"],
            "DOGE": ["dogecoin", "doge"],
            "GOLD": ["gold"],
            "SILVER": ["silver"],
            "OIL": ["oil", "crude", "wti", "brent"],
            "NATGAS": ["natural gas", "natgas"],
            "COPPER": ["copper"],
        }

        keywords = company_map.get(ticker.upper(), [ticker.lower()])

        for feed in RSS_FEEDS:
            try:
                parsed_feed = feedparser.parse(feed["url"])

                for entry in parsed_feed.entries:
                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    link = entry.get("link", "")

                    combined_text = f"{title} {summary}".lower()

                    if not any(keyword.lower() in combined_text for keyword in keywords):
                        continue

                    items.append({
                        "title": title,
                        "publisher": feed["name"],
                        "link": link,
                        "source_type": self.source_type,
                        "text": f"{title}. {summary}",
                    })

                    if len(items) >= limit:
                        return items

            except Exception as e:
                print(f"RSS source error for {feed['name']}: {e}")

        return items