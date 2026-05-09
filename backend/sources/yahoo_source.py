import yfinance as yf
from sources.base_source import MarketSource

class YahooSource(MarketSource):
    name = "Yahoo Finance"
    source_type = "Yahoo News"

    def fetch(self, ticker: str, limit: int = 10):
        stock = yf.Ticker(ticker)
        raw_news = stock.news[:limit]

        items = []

        for item in raw_news:
            content = item.get("content", {})

            title = content.get("title", "")
            publisher = content.get("provider", {}).get("displayName", "")
            link = content.get("canonicalUrl", {}).get("url", "")

            items.append({
                "title": title,
                "publisher": publisher,
                "link": link,
                "source_type": self.source_type,
                "text": title
            })

        return items