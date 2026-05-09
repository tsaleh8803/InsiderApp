def get_source_weight(publisher: str, source_type: str):
    publisher = publisher.lower()
    source_type = source_type.lower()

    high_weight_sources = [
        "reuters",
        "wall street journal",
        "barrons",
        "barron's",
        "zacks",
        "investor's business daily",
        "cnbc",
        "marketwatch"
    ]

    medium_weight_sources = [
        "yahoo finance",
        "benzinga",
        "gurufocus",
        "24/7 wall st",
        "simply wall st"
    ]

    if any(source in publisher for source in high_weight_sources):
        return 1.0

    if any(source in publisher for source in medium_weight_sources):
        return 0.75
    
    if "rss news" in source_type:
        return 0.85
    
    if "sec filing" in source_type:
        return 1.0

    if "reddit" in source_type:
        return 0.45

    if "youtube" in source_type:
        return 0.40

    return 0.60


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