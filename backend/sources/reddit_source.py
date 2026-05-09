import requests
from sources.base_source import MarketSource

class RedditSource(MarketSource):
    name = "Reddit"
    source_type = "Reddit"

    def fetch(self, ticker: str, limit: int = 10):
        query = f"{ticker} stock OR {ticker} earnings OR {ticker} shares"
        url = "https://www.reddit.com/search.json"

        headers = {
            "User-Agent": "insider-app-prototype/0.1"
        }

        params = {
            "q": query,
            "sort": "new",
            "limit": limit
        }

        items = []

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=10
            )

            data = response.json()
            posts = data.get("data", {}).get("children", [])

            for post in posts:
                post_data = post.get("data", {})

                title = post_data.get("title", "")
                subreddit = post_data.get("subreddit", "")
                permalink = post_data.get("permalink", "")

                items.append({
                    "title": title,
                    "publisher": f"r/{subreddit}",
                    "link": f"https://www.reddit.com{permalink}",
                    "source_type": self.source_type,
                    "text": title
                })

        except Exception as e:
            print(f"Reddit source error: {e}")

        return items