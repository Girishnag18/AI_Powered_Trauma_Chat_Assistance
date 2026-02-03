from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

CRITICAL = ["suicide", "kill myself", "end my life"]
HIGH = ["hopeless", "panic", "worthless"]

def analyze(text):
    sentiment = sia.polarity_scores(text)["compound"]

    if any(w in text.lower() for w in CRITICAL):
        return 90, "Critical"

    if any(w in text.lower() for w in HIGH):
        return 70, "High"

    if sentiment <= -0.6:
        return 60, "High"
    elif sentiment <= -0.3:
        return 45, "Moderate"

    return 20, "Low"

def reply(severity):
    responses = {
        "Low": "I’m glad you shared this. Want to tell me more?",
        "Moderate": "That sounds difficult. I’m here with you.",
        "High": "I’m concerned. Reaching out to someone may really help.",
        "Critical": "Your safety matters. Please contact a professional or helpline immediately."
    }
    return responses[severity]
