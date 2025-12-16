def get_tone(option):
    return {
        "Neutral": "neutral and factual",
        "Bullish": "optimistic and growth focused",
        "Bearish": "risk-aware and cautious"
    }[option]


def get_length(option):
    return {
        "Short": "5–6 bullet points",
        "Medium": "8–10 bullet points",
        "Detailed": "detailed structured analysis"
    }[option]
