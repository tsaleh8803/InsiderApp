import requests
import feedparser
from sources.base_source import MarketSource


class CryptoSource(MarketSource):
    name = "Crypto Intelligence"
    source_type = "Crypto News"

    CRYPTO_RSS_FEEDS = [
        {
            "name": "CoinDesk",
            "url": "https://www.coindesk.com/arc/outboundfeeds/rss/",
        },
        {
            "name": "CoinTelegraph",
            "url": "https://cointelegraph.com/rss",
        },
        {
            "name": "Decrypt",
            "url": "https://decrypt.co/feed",
        },
    ]

    COINGECKO_URL = "https://api.coingecko.com/api/v3/search/trending"

    CRYPTO_KEYWORDS = {
        "BTC": ["bitcoin", "btc"],
        "ETH": ["ethereum", "eth"],
        "SOL": ["solana", "sol"],
        "DOGE": ["dogecoin", "doge"],
        "XRP": ["xrp", "ripple"],
        "ADA": ["cardano", "ada"],
        "AVAX": ["avalanche", "avax"],
    }

    def fetch(self, ticker: str, limit: int = 10):
        ticker = ticker.upper()

        keywords = self.CRYPTO_KEYWORDS.get(
            ticker,
            [ticker.lower()]
        )

        items = []

        items.extend(
            self.get_crypto_rss_news(
                ticker=ticker,
                keywords=keywords,
                limit=limit
            )
        )

        items.extend(
            self.get_trending_mentions(
                ticker=ticker,
                keywords=keywords
            )
        )

        return items[:limit]

    def get_crypto_rss_news(self, ticker, keywords, limit):
        items = []

        for feed in self.CRYPTO_RSS_FEEDS:
            try:
                parsed_feed = feedparser.parse(feed["url"])

                for entry in parsed_feed.entries:
                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    link = entry.get("link", "")

                    combined_text = (
                        f"{title} {summary}"
                    ).lower()

                    if not any(
                        keyword.lower() in combined_text
                        for keyword in keywords
                    ):
                        continue

                    items.append({
                        "title": title,
                        "publisher": feed["name"],
                        "link": link,
                        "source_type": self.source_type,
                        "text": f"{title}. {summary}",
                        "market_sector": "Crypto",
                    })

                    if len(items) >= limit:
                        return items

            except Exception as e:
                print(f"Crypto RSS error ({feed['name']}): {e}")

        return items

    def get_trending_mentions(self, ticker, keywords):
        items = []

        try:
            response = requests.get(
                self.COINGECKO_URL,
                timeout=10
            )

            data = response.json()

            coins = data.get("coins", [])

            for coin in coins:
                item = coin.get("item", {})

                name = item.get("name", "")
                symbol = item.get("symbol", "")
                market_cap_rank = item.get("market_cap_rank", "")
                score = item.get("score", "")

                combined_text = (
                    f"{name} {symbol}"
                ).lower()

                if not any(
                    keyword.lower() in combined_text
                    for keyword in keywords
                ):
                    continue

                items.append({
                    "title": (
                        f"{name} is trending on CoinGecko "
                        f"(rank #{market_cap_rank})"
                    ),
                    "publisher": "CoinGecko",
                    "link": "https://www.coingecko.com/",
                    "source_type": self.source_type,
                    "text": (
                        f"{name} crypto asset is trending "
                        f"on CoinGecko."
                    ),
                    "market_sector": "Crypto",
                    "trend_score": score,
                })

        except Exception as e:
            print(f"CoinGecko trending error: {e}")

        return items