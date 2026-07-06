SOURCE_WEIGHTS = {
    # High trust / primary-ish financial sources
    "reuters": 1.0,
    "wall street journal": 1.0,
    "wsj": 1.0,
    "barrons": 1.0,
    "barron's": 1.0,
    "zacks": 1.0,
    "investor's business daily": 1.0,
    "ibd": 1.0,
    "cnbc": 1.0,
    "marketwatch": 1.0,
    "sec edgar": 1.0,

    # Medium/high financial sources
    "yahoo finance": 0.75,
    "benzinga": 0.75,
    "gurufocus": 0.75,
    "24/7 wall st": 0.75,
    "simply wall st": 0.75,
    "investing.com": 0.75,

    # Crypto-specific sources
    "coindesk": 0.80,
    "cointelegraph": 0.80,
    "decrypt": 0.80,
    "coingecko": 0.75,

    # Social / creator sources
    "reddit": 0.45,
    "youtube": 0.40,
    "stocktwits": 0.45,
}

SOURCE_TYPE_DEFAULTS = {
    "yahoo news": 0.75,
    "rss news": 0.85,
    "reddit": 0.45,
    "youtube": 0.40,
    "sec filing": 1.0,
    "crypto news": 0.80,
}


def get_source_weight(publisher: str, source_type: str):
    publisher = (publisher or "").lower().strip()
    source_type = (source_type or "").lower().strip()

    for source_name, weight in SOURCE_WEIGHTS.items():
        if source_name in publisher:
            return weight

    return SOURCE_TYPE_DEFAULTS.get(source_type, 0.60)


def calculate_weighted_score(articles):
    if not articles:
        return 0

    weighted_sum = 0
    total_weight = 0

    for article in articles:
        weight = article.get("source_weight", 1)
        score = article.get("score", 0)

        weighted_sum += score * weight
        total_weight += weight

    if total_weight == 0:
        return 0

    return round(weighted_sum / total_weight, 3)


def convert_to_ai_score(average_score):
    score = ((average_score + 1) / 2) * 100
    return max(0, min(100, round(score)))


def get_signal_from_ai_score(ai_score):
    if ai_score >= 70:
        return "Bullish"
    if ai_score <= 40:
        return "Bearish"
    return "Neutral"


def get_confidence(articles):
    count = len(articles)

    if count >= 10:
        return "High"
    if count >= 5:
        return "Medium"
    if count >= 1:
        return "Low"

    return "No Data"