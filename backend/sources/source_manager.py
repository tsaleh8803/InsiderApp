from sources.yahoo_source import YahooSource
from sources.reddit_source import RedditSource
from sources.youtube_source import YouTubeSource
from sources.rss_source import RSSSource
from sources.sec_source import SECSource
from sources.crypto_source import CryptoSource

SOURCES = [
    YahooSource(),
    RSSSource(),
    RedditSource(),
    YouTubeSource(),
    SECSource(),
    CryptoSource(),
]

SOURCE_LIMITS = {
    "Yahoo News": 10,
    "RSS News": 10,
    "Reddit": 10,
    "YouTube": 5,
    "SEC Filing": 5,
}


def collect_all_sources(ticker: str):
    all_items = []

    for source in SOURCES:
        limit = SOURCE_LIMITS.get(source.source_type, 10)

        try:
            items = source.fetch(ticker=ticker, limit=limit)
            all_items.extend(items)

        except Exception as e:
            print(f"{source.name} failed: {e}")

    return all_items