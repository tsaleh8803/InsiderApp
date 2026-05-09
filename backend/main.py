from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sources.source_manager import collect_all_sources
from sentiment import classify_sentiment
from database import create_tables, save_article_analysis, get_history
from relevance import is_relevant_to_ticker
from scoring import get_source_weight, calculate_weighted_score

app = FastAPI(title="Insider App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://10.168.140.152:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()


@app.get("/")
def home():
    return {"message": "Insider App API is running"}


@app.get("/analyze/{ticker}")
def analyze_ticker(ticker: str):
    ticker = ticker.upper()

    articles = collect_all_sources(ticker)

    results = []

    for article in articles:
        title = article["title"]
        text_to_analyze = article["text"]
        if not is_relevant_to_ticker(ticker, article["text"]):
            continue

        label, score = classify_sentiment(text_to_analyze) #FinBERT analysis

        source_weight = get_source_weight(
            article["publisher"],
            article["source_type"]
        )

        analyzed_article = {
            "title": title,
            "publisher": article["publisher"],
            "link": article["link"],
            "source_type": article["source_type"],
            "sentiment": label,
            "score": score,
            "source_weight": source_weight,
            "weighted_score": round(score * source_weight, 3),
            "filing_type": article.get("filing_type"),
            "filing_date": article.get("filing_date"),
            "event_type": article.get("event_type"),
            "importance": article.get("importance"),
        }
        results.append(analyzed_article)

        save_article_analysis(ticker, analyzed_article)

    if len(results) == 0:
        return {
            "ticker": ticker,
            "overall_signal": "No Data",
            "average_score": 0,
            "bullish_count": 0,
            "bearish_count": 0,
            "neutral_count": 0,
            "articles": []
        }

    average_score = calculate_weighted_score(results)

    if average_score >= 0.2:
        overall_signal = "Bullish"
    elif average_score <= -0.2:
        overall_signal = "Bearish"
    else:
        overall_signal = "Neutral"

    return {
        "ticker": ticker,
        "overall_signal": overall_signal,
        "average_score": round(average_score, 3),
        "bullish_count": sum(1 for item in results if item["sentiment"] == "Bullish"),
        "bearish_count": sum(1 for item in results if item["sentiment"] == "Bearish"),
        "neutral_count": sum(1 for item in results if item["sentiment"] == "Neutral"),
        "articles": results
    }


@app.get("/history/{ticker}")
def ticker_history(ticker: str):
    ticker = ticker.upper()

    history = get_history(ticker)

    return {
        "ticker": ticker,
        "count": len(history),
        "history": [
            {
                "title": item.title,
                "publisher": item.publisher,
                "link": item.link,
                "sentiment": item.sentiment,
                "score": item.score,
                "created_at": item.created_at
            }
            for item in history
        ]
    }