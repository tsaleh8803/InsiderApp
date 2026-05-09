import yfinance as yf

def get_news(ticker: str, limit: int = 10):
    stock = yf.Ticker(ticker)
    raw_news = stock.news[:limit]

    articles = []

    for item in raw_news:
        content = item.get("content", {})

        title = content.get("title", "")
        publisher = content.get("provider", {}).get("displayName", "")
        link = content.get("canonicalUrl", {}).get("url", "")

        articles.append({
            "title": title,
            "publisher": publisher,
            "link": link
        })

    return articles