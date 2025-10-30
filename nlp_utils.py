from textblob import TextBlob
import re

# List of filler words
FILLER_WORDS = ["um", "uh", "like", "you know", "so", "actually", "basically", "literally"]

# Keywords you're expected to mention in interview
TECH_KEYWORDS = ["angular", "python", "machine learning", "data", "project", "api", "model"]

def analyze_text(text):
    analysis = {}

    # Filler word detection
    filler_count = {}
    for word in FILLER_WORDS:
        count = len(re.findall(r"\b" + re.escape(word) + r"\b", text.lower()))
        if count > 0:
            filler_count[word] = count
    analysis["filler_words"] = filler_count

    # Sentiment detection
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    tone = "Positive" if polarity > 0.2 else "Negative" if polarity < -0.2 else "Neutral"
    analysis["sentiment"] = {"tone": tone, "score": polarity}

    # Keyword detection
    found_keywords = [kw for kw in TECH_KEYWORDS if kw in text.lower()]
    analysis["keywords_found"] = found_keywords
    analysis["keywords_missing"] = list(set(TECH_KEYWORDS) - set(found_keywords))

    return analysis
