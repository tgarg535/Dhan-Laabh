import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import yfinance as yf
import feedparser
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# --- NLTK DATA SETUP ---
# This will download the necessary NLTK models if they are not already present.
try:
    stopwords.words('english')
except LookupError:
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK punkt tokenizer...")
    nltk.download('punkt')


# --- TEXT PREPROCESSING UTILITY (UPDATED) ---
def preprocess_text(text):
    """
    Cleans and preprocesses a given text using the NLTK library.
    - Converts to lowercase
    - Tokenizes text (splits into words)
    - Removes punctuation and non-alphabetic characters
    - Removes common English stop words
    
    Args:
        text (str): The raw text string.
        
    Returns:
        list: A list of cleaned and tokenized words.
    """
    if not isinstance(text, str):
        return []

    # 1. Convert to lowercase and tokenize using NLTK's word tokenizer
    tokens = word_tokenize(text.lower())
    
    # 2. Get the standard set of English stop words from NLTK
    stop_words = set(stopwords.words('english'))
    
    # 3. Filter out stop words and any tokens that are not purely alphabetic (removes punctuation and numbers)
    cleaned_tokens = [
        word for word in tokens 
        if word.isalpha() and word not in stop_words
    ]
    
    return cleaned_tokens

# --- SCRAPER CONFIGURATION ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5.0 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# --- GOOGLE NEWS SCRAPER ---
def scrape_google_news(symbol, company_name):
    """
    Scrapes financial news headlines using the Google News RSS feed.
    """
    query = f'"{company_name}" OR "{symbol}" stock'
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
    
    headlines = []
    
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            headlines.append(entry.title)
        return headlines

    except Exception as e:
        print(f"❌ Error fetching or parsing Google News RSS feed for {symbol}: {e}")
        return []

# --- REDDIT SCRAPER ---
def scrape_reddit(symbol, company_name):
    """
    Scrapes recent post titles mentioning the stock from relevant subreddits.
    """
    subreddits = ["investing", "stocks", "wallstreetbets"]
    titles = []
    simple_name = company_name.split(' ')[0].replace(',', '')

    for subreddit in subreddits:
        try:
            query = f'"{symbol}" OR "{simple_name}"'
            url = f"https://www.reddit.com/r/{subreddit}/search.json?q={urllib.parse.quote(query)}&sort=new&limit=5&restrict_sr=on"
            
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data and 'children' in data['data']:
                for post in data['data']['children']:
                    titles.append(post['data']['title'])

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching Reddit data from r/{subreddit} for {symbol}: {e}")
            continue

    return titles

# --- MAIN SCRAPER FUNCTION ---
def scrape_financial_news(symbol):
    """
    Main function to orchestrate scraping from all sources and combine the results.
    """
    print(f"\n--- Scraping news and social media for {symbol} ---")
    
    company_name = symbol
    try:
        company_info = yf.Ticker(symbol).info
        company_name = company_info.get('longName', symbol)
    except Exception as e:
        print(f"Could not fetch company longName for {symbol}: {e}")
        
    google_headlines = scrape_google_news(symbol, company_name)
    reddit_headlines = scrape_reddit(symbol, company_name)
    
    combined_headlines = google_headlines + reddit_headlines
    
    if not combined_headlines:
        print(f"⚠️ No headlines found for {symbol}. Using placeholder data.")
        return [f"Market is quiet for {symbol} today.", f"Investors watch {symbol} closely for new developments."]
        
    print(f"✅ Found {len(combined_headlines)} total headlines for {symbol}.")
    return combined_headlines
