# Import the VADER sentiment analysis tool
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- INITIALIZATION ---
# Create a single, reusable analyzer object
# This is fast and takes up very little memory
analyzer = SentimentIntensityAnalyzer()

# --- SENTIMENT ANALYSIS FUNCTION ---

def get_sentiment(headlines):
    """
    Analyzes the sentiment of a list of news headlines using the VADER model.
    """
    if not headlines:
        return {"overall_sentiment": "Neutral", "positive_headlines": 0, "negative_headlines": 0, "neutral_headlines": 0, "headlines": []}

    analyzed_headlines = []
    pos_count, neg_count, neu_count = 0, 0, 0
    
    for headline in headlines:
        # Get the sentiment scores from VADER. It returns a dictionary.
        # e.g., {'neg': 0.0, 'neu': 0.588, 'pos': 0.412, 'compound': 0.4404}
        scores = analyzer.polarity_scores(headline)
        
        # The 'compound' score is a single, normalized score from -1 (most negative) to +1 (most positive).
        # We can use it to determine the overall sentiment.
        compound_score = scores['compound']
        
        if compound_score >= 0.05:
            sentiment = "Positive"
            pos_count += 1
        elif compound_score <= -0.05:
            sentiment = "Negative"
            neg_count += 1
        else:
            sentiment = "Neutral"
            neu_count += 1
        
        analyzed_headlines.append({"text": headline, "sentiment": sentiment})

    # Determine the overall sentiment based on the majority vote
    if pos_count > neg_count and pos_count > neu_count: overall = "Positive"
    elif neg_count > pos_count and neg_count > neu_count: overall = "Negative"
    else: overall = "Neutral"

    return {
        "overall_sentiment": overall,
        "positive_headlines": pos_count,
        "negative_headlines": neg_count,
        "neutral_headlines": neu_count,
        "headlines": analyzed_headlines,
    }
