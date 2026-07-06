from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="ProsusAI/finbert"
)

def classify_sentiment(text: str):
    if not text or text.strip() == "":
        return "Neutral", 0.0

    result = classifier(text[:512])[0]

    label = result["label"].lower()
    confidence = result["score"]

    if label == "positive":
        sentiment = "Bullish"
        score = confidence
    elif label == "negative":
        sentiment = "Bearish"
        score = -confidence
    else:
        sentiment = "Neutral"
        score = 0.0

    return sentiment, round(score, 3)