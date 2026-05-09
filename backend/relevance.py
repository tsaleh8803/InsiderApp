def is_relevant_to_ticker(ticker: str, text: str):
    ticker = ticker.lower()
    text = text.lower()

    keyword_map = {
        "TSLA": ["tesla", "tsla", "elon", "robotaxi"],
        "NVDA": ["nvidia", "nvda", "gpu", "ai chip"],
        "AAPL": ["apple", "iphone", "ios"],
        "BTC": ["bitcoin", "btc", "crypto"],
        "ETH": ["ethereum", "eth"]
    }

    keywords = keyword_map.get(ticker.upper(), [ticker])

    matches = 0

    for keyword in keywords:
        if keyword.lower() in text:
            matches += 1

    return matches > 0