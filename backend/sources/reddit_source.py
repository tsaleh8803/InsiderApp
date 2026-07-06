import requests
from sources.base_source import MarketSource


class RedditSource(MarketSource):
    name = "Reddit"
    source_type = "Reddit"

    QUERY_MAP = {
        "TSLA": "TSLA OR Tesla stock OR Tesla earnings OR Tesla robotaxi",
        "NVDA": "NVDA OR Nvidia stock OR Nvidia earnings OR AI chips",
        "AAPL": "AAPL OR Apple stock OR iPhone sales",
        "MSFT": "MSFT OR Microsoft stock OR Azure earnings",
        "AMZN": "AMZN OR Amazon stock OR AWS earnings",
        "META": "META OR Meta stock OR Facebook Instagram earnings",
        "GOOGL": "GOOGL OR Google stock OR Alphabet earnings",

        "BTC": "Bitcoin OR BTC price OR crypto market",
        "ETH": "Ethereum OR ETH price OR crypto market",
        "SOL": "Solana OR SOL price OR crypto market",
        "DOGE": "Dogecoin OR DOGE price OR crypto market",

        "GOLD": "gold price OR XAUUSD OR bullion OR precious metals",
        "SILVER": "silver price OR XAGUSD OR precious metals",
        "OIL": "oil price OR crude oil OR WTI OR Brent",
        "NATGAS": "natural gas price OR LNG OR natgas futures",
        "COPPER": "copper price OR copper futures OR copper supply",
    }

    def fetch(self, ticker: str, limit: int = 10):
        ticker = ticker.upper()

        query = self.QUERY_MAP.get(
            ticker,
            f"{ticker} stock OR {ticker} earnings OR {ticker} shares"
        )

        url = "https://www.reddit.com/search.json"

        headers = {
            "User-Agent": "insider-app-prototype/0.1"
        }

        params = {
            "q": query,
            "sort": "new",
            "limit": limit,
        }

        items = []

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=10,
            )

            response.raise_for_status()
            data = response.json()

            posts = data.get("data", {}).get("children", [])

            for post in posts:
                post_data = post.get("data", {})

                title = post_data.get("title", "")
                subreddit = post_data.get("subreddit", "")
                permalink = post_data.get("permalink", "")
                selftext = post_data.get("selftext", "")
                score = post_data.get("score", 0)
                comments = post_data.get("num_comments", 0)

                if not title:
                    continue

                items.append({
                    "title": title,
                    "publisher": f"r/{subreddit}",
                    "link": f"https://www.reddit.com{permalink}",
                    "source_type": self.source_type,
                    "text": f"{title}. {selftext[:500]}",
                    "reddit_score": score,
                    "reddit_comments": comments,
                })

        except Exception as e:
            print(f"Reddit source error: {e}")

        return items