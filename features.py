"""Ticker and lexicon processing excerpt; no AI or model training."""
import re
from datetime import datetime, timezone
UTC = timezone.utc

def timestamp(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Timestamps must include a timezone")
    return result.astimezone(UTC)

def stamp(value):
    return value.astimezone(UTC).isoformat()

def extract_tickers(text, universe):
    # Bare tickers must be uppercase; ambiguous words need a dollar sign.
    ambiguous = {"A", "I", "IT", "ON", "ALL", "FOR", "ARE", "NOW", "CEO", "DD", "AI"}
    matches = re.findall(r"(?<![\w$])(\$?[A-Za-z]{1,5}(?:[./][A-Za-z])?)(?!\w)", text)
    return sorted({m.lstrip("$").upper() for m in matches
                   if m.lstrip("$").upper() in universe
                   and (m.startswith("$") or (m.isupper() and m not in ambiguous))})

def sentiment(text):
    positive = {"bullish", "buy", "growth", "beat", "strong", "rally", "upside", "breakout", "profit"}
    negative = {"bearish", "sell", "weak", "miss", "downside", "crash", "overvalued", "loss", "dump"}
    words = re.findall(r"[a-z]+|[,.!?;]", text.lower())
    score = count = 0
    for i, word in enumerate(words):
        value = int(word in positive) - int(word in negative)
        if value:
            preceding = words[max(0, i-3):i]
            for j, w in enumerate(preceding):
                if w in {",", ".", "!", "?", ";"}:
                    preceding = preceding[j+1:]
            if any(w in {"not", "never", "no"} for w in preceding):
                value *= -1
            score += value
            count += 1
    return score / max(1, count)
