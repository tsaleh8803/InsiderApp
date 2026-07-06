import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from sources.base_source import MarketSource
from datetime import datetime, timedelta, timezone

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
            "GOLD": "gold price news XAUUSD precious metals analysis",
        }

        query = query_map.get(
            ticker.upper(),
            f"{ticker} stock news analysis"
        )

        items = []

        try:
            youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
            one_week_ago = (
                datetime.now(timezone.utc) - timedelta(days=7)
            ).isoformat()
            
            # Search for videos
            search_request = youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=20,
                order="relevance",
                publishedAfter=one_week_ago,
            )

            search_response = search_request.execute()

            video_ids = [
                item["id"]["videoId"]
                for item in search_response.get("items", [])
            ]

            # Fetch video statistics
            stats_request = youtube.videos().list(
                part="statistics,snippet",
                id=",".join(video_ids),
            )

            stats_response = stats_request.execute()

            for video in stats_response.get("items", []):

                snippet = video["snippet"]
                stats = video["statistics"]

                title = snippet.get("title", "")
                description = snippet.get("description", "")
                channel = snippet.get("channelTitle", "")
                video_id = video["id"]

                views = int(stats.get("viewCount", 0))
                likes = int(stats.get("likeCount", 0))

                # -------- QUALITY FILTERS --------

                # Minimum views
                if views < 10000:
                    continue

                # Avoid low engagement spam
                like_ratio = likes / views if views > 0 else 0

                if like_ratio < 0.01:
                    continue

                # Avoid obvious clickbait
                bad_words = [
                    "1000x",
                    "guaranteed",
                    "must buy now",
                    "urgent",
                    "insane gains",
                    "crazy profits",
                ]

                lowered = title.lower()

                if any(word in lowered for word in bad_words):
                    continue

                # Prefer credible finance channels
                credibility_boost = 0

                trusted_channels = [
                    "Bloomberg",
                    "CNBC",
                    "Yahoo Finance",
                    "The Wall Street Journal",
                    "Investor's Business Daily",
                    "MarketWatch",
                    "Benzinga",
                    "New Money",
                    "Meet Kevin",
                ]

                if any(
                    trusted.lower() in channel.lower()
                    for trusted in trusted_channels
                ):
                    credibility_boost = 1

                link = f"https://www.youtube.com/watch?v={video_id}"

                items.append({
                    "title": title,
                    "publisher": channel,
                    "link": link,
                    "source_type": self.source_type,
                    "views": views,
                    "likes": likes,
                    "credibility_boost": credibility_boost,
                    "text": f"{title}. {description}",
                })

            # Sort by credibility + views
            items.sort(
                key=lambda x: (
                    x["credibility_boost"],
                    x["views"]
                ),
                reverse=True
            )

            return items[:limit]

        except Exception as e:
            print(f"YouTube source error: {e}")

        return []