import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from sources.base_source import MarketSource

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


class YouTubeSource(MarketSource):
    name = "YouTube"
    source_type = "YouTube"

    def fetch(self, ticker: str, limit: int = 5):
        if not YOUTUBE_API_KEY:
            print("YouTube API key not found")
            return []

        query_map = {
            "TSLA": "Tesla stock news analysis",
            "NVDA": "Nvidia stock news analysis",
            "AAPL": "Apple stock news analysis",
            "MSFT": "Microsoft stock news analysis",
            "AMZN": "Amazon stock news analysis",
            "META": "Meta stock news analysis",
            "GOOGL": "Google Alphabet stock news analysis",
            "BTC": "Bitcoin price news analysis",
            "ETH": "Ethereum price news analysis",
            "SOL": "Solana price news analysis",
            "DOGE": "Dogecoin price news analysis",
            "GOLD": "Gold commodity price news analysis",
            "SILVER": "Silver commodity price news analysis",
            "OIL": "Crude oil price news analysis",
            "NATGAS": "Natural gas commodity news analysis",
            "COPPER": "Copper commodity price news analysis",
        }

        query = query_map.get(ticker.upper(), f"{ticker} stock news analysis")

        items = []

        try:
            youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

            request = youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=limit,
                order="date",
            )

            response = request.execute()

            for video in response.get("items", []):
                video_id = video["id"]["videoId"]
                snippet = video["snippet"]

                title = snippet.get("title", "")
                channel = snippet.get("channelTitle", "")
                description = snippet.get("description", "")
                link = f"https://www.youtube.com/watch?v={video_id}"

                if not title:
                    continue

                items.append({
                    "title": title,
                    "publisher": channel,
                    "link": link,
                    "source_type": self.source_type,
                    "text": f"{title}. {description}",
                })

        except Exception as e:
            print(f"YouTube source error: {e}")

        return items