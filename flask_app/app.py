import os
import joblib
from flask import Flask, render_template, request, jsonify
from sentiment_analysis.scraper import scrape_financial_news, preprocess_text
from sentiment_analysis.analyzer import get_sentiment
import yfinance as yf
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

# --- CONFIGURATION ---
MODEL_DIR = 'models/best_models'
TOP_10_COMPANIES = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "META", "NFLX", "NVDA", "JPM", "V"]
NEWSDATA_API_KEY = "pub_94577a15656449d68343f8d0b1c9d935"

STOCKS_INFO = {
    "AAPL": {"name": "Apple Inc.", "logo": "https://logo.clearbit.com/apple.com", "website": "https://www.apple.com"},
    "MSFT": {"name": "Microsoft Corp.", "logo": "https://logo.clearbit.com/microsoft.com", "website": "https://www.microsoft.com"},
    "GOOG": {"name": "Alphabet Inc.", "logo": "https://logo.clearbit.com/abc.xyz", "website": "https://abc.xyz"},
    "GOOGL": {"name": "Alphabet Inc.", "logo": "https://logo.clearbit.com/abc.xyz", "website": "https://abc.xyz"},
    "AMZN": {"name": "Amazon.com, Inc.", "logo": "https://logo.clearbit.com/amazon.com", "website": "https://www.amazon.com"},
    "TSLA": {"name": "Tesla, Inc.", "logo": "https://logo.clearbit.com/tesla.com", "website": "https://www.tesla.com"},
    "META": {"name": "Meta Platforms, Inc.", "logo": "https://logo.clearbit.com/meta.com", "website": "https://www.meta.com"},
    "NFLX": {"name": "Netflix, Inc.", "logo": "https://logo.clearbit.com/netflix.com", "website": "https://www.netflix.com"},
    "NVDA": {"name": "NVIDIA Corp.", "logo": "https://logo.clearbit.com/nvidia.com", "website": "https://www.nvidia.com"},
    "JPM": {"name": "JPMorgan Chase & Co.", "logo": "https://logo.clearbit.com/jpmorganchase.com", "website": "https://www.jpmorganchase.com"},
    "V": {"name": "Visa Inc.", "logo": "https://logo.clearbit.com/visa.com", "website": "https://www.visa.com"}
}

# --- HELPER FUNCTIONS ---
def load_model(symbol):
    symbol = symbol.upper()
    model_path = os.path.join(MODEL_DIR, f'{"generalized_model" if symbol not in TOP_10_COMPANIES else symbol}.pkl')
    if not os.path.exists(model_path): return None
    try: return joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model {model_path}: {e}")
        return None

def get_stock_prediction(symbol, headlines):
    model = load_model(symbol)
    if model is None: return {"prediction": "N/A", "confidence": 0, "error": "Model not available."}
    
    all_processed_words = []
    for text in headlines:
        all_processed_words.extend(preprocess_text(text))
    
    # Placeholder for actual prediction using processed words
    import random
    prediction_price = round(random.uniform(150, 500), 2)
    confidence_score = round(random.uniform(0.75, 0.95), 2)
    return {"prediction": f"${prediction_price}", "confidence": f"{int(confidence_score * 100)}%"}

# --- MAIN ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how-it-works.html')

@app.route('/predict', methods=['POST'])
def predict():
    stock_symbol = request.form.get('stock_symbol', '').strip().upper()
    if not stock_symbol: return render_template('index.html', error="Please enter a stock symbol.")
    
    company_name = stock_symbol
    try:
        company_info = yf.Ticker(stock_symbol).info
        company_name = company_info.get('longName', stock_symbol)
    except Exception:
        pass # Keep default name if fetch fails

    news_headlines = scrape_financial_news(stock_symbol)
    
    # --- DEBUGGING: PRINT SCRAPED HEADLINES ---
    print("\n" + "="*50)
    print(f"SCRAPED HEADLINES FOR: {stock_symbol}")
    print("="*50)
    if news_headlines:
        for i, headline in enumerate(news_headlines):
            print(f"{i+1}: {headline}")
    else:
        print("!!! No headlines were found. !!!")
    print("="*50 + "\n")
    # --- END DEBUGGING ---

    prediction_data = get_stock_prediction(stock_symbol, news_headlines)
    sentiment_data = get_sentiment(news_headlines)
    
    return render_template('result.html', 
                           symbol=stock_symbol, 
                           company_name=company_name,
                           prediction=prediction_data, 
                           sentiment=sentiment_data)

# --- API ROUTES ---
@app.route('/api/market-data')
def market_data():
    try:
        tickers = yf.Tickers(list(STOCKS_INFO.keys()))
        data = []
        for symbol, info in STOCKS_INFO.items():
            stock_data = tickers.tickers[symbol].history(period='2d')
            if not stock_data.empty and len(stock_data) > 1:
                latest = stock_data.iloc[-1]
                prev_close = stock_data.iloc[-2]['Close']
                data.append({
                    "symbol": symbol, "name": info["name"], "logo": info["logo"], "website": info["website"],
                    "price": latest['Close'], "change": latest['Close'] - prev_close,
                    "changePercent": ((latest['Close'] - prev_close) / prev_close) * 100,
                    "dayHigh": latest['High'], "dayLow": latest['Low'], "volume": latest['Volume']
                })
        return jsonify(data)
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/api/historical-data/<symbol>')
def get_historical_data(symbol):
    period = request.args.get('period', '1y')
    try:
        hist = yf.Ticker(symbol).history(period=period)
        if hist.empty: return jsonify({"dates": [], "prices": []})
        hist.index = hist.index.strftime('%Y-%m-%d')
        return jsonify({"dates": list(hist.index), "prices": list(hist['Close'])})
    except Exception as e: return jsonify({"error": str(e)}), 500

@app.route('/api/predict-future/<symbol>')
def predict_future(symbol):
    try:
        start_price = yf.Ticker(symbol).history(period='1d')['Close'].iloc[0]
        today = datetime.now()
        dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 61)]
        import random
        prices = [start_price * (1 + random.uniform(-0.02, 0.02)) for _ in range(60)]
        return jsonify({"dates": dates, "prices": prices})
    except Exception as e:
        return jsonify({"error": str(e), "dates": [], "prices": []}), 500

@app.route('/api/news/<symbol>')
def get_news(symbol):
    company_name = STOCKS_INFO.get(symbol.upper(), {}).get('name', symbol)
    query = f'("{company_name}" OR "{symbol}")'
    url = (f"https://newsdata.io/api/1/news?"
           f"apikey={NEWSDATA_API_KEY}&"
           f"language=en&"
           f"category=business,technology")
    
    print(f"Fetching news from URL: {url}") # Debug print
    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()

        if news_data.get('status') == 'error':
            print(f"Newsdata.io API Error: {news_data.get('message')}")
            return jsonify({"error": news_data.get('message')}), 500
        
        print(f"Found {len(news_data.get('results', []))} articles for {symbol}")
        return jsonify(news_data.get('results', []))
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch news: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)