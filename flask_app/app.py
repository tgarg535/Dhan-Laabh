import os
import numpy as np
import pandas as pd
import yfinance as yf
from flask import Flask, render_template, request, jsonify
from sentiment_analysis.scraper import scrape_financial_news
from sentiment_analysis.analyzer import get_sentiment
from datetime import datetime, timedelta
import requests
import pickle
import tensorflow as tf
import urllib.parse

app = Flask(__name__)

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, 'artifacts')

TOP_10_COMPANIES = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "META", "NFLX", "NVDA", "JPM", "V"]
NEWSDATA_API_KEY = os.getenv('NEWSDATA_API_KEY')  # Ensure
TIME_STEP = 60  # Must match training

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

# --- UTILITY CLASS ---
class MainUtils:
    @staticmethod
    def load_object(file_path):
        try:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            print(f"❌ Error loading object from {file_path}: {e}")
            return None

# --- MODEL LOGIC ---
def get_model_and_scaler(symbol):
    symbol = symbol.upper()
    if symbol in TOP_10_COMPANIES:
        model_path = os.path.join(ARTIFACTS_DIR, "models", "best_models", f"best_model_{symbol}.h5")
        scaler_path = os.path.join(ARTIFACTS_DIR, "scalers", "stock_scalers", f"{symbol}_scaler.pkl")
    else:
        model_path = os.path.join(ARTIFACTS_DIR, "models", "best_models", "best_model_general.h5")
        scaler_path = os.path.join(ARTIFACTS_DIR, "scalers", "general_stock_scalers", "general_stock_scaler.pkl")

    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        print("File not found:", model_path, scaler_path)
        return None, None
    try:
        model = tf.keras.models.load_model(model_path)
        scaler = MainUtils.load_object(scaler_path)
        return model, scaler
    except Exception as e:
        print(f"Error loading model/scaler: {e}")
        return None, None

def get_stock_prediction(symbol):
    model, scaler = get_model_and_scaler(symbol)
    if model is None or scaler is None:
        return {"prediction": "N/A", "confidence": "N/A", "error": "Model or scaler not found."}
    try:
        df = yf.download(symbol, period="100d", interval="1d")
        if len(df) < TIME_STEP:
            return {"prediction": "N/A", "confidence": "N/A", "error": "Not enough historical data."}

        last_days = df[['Close']].tail(TIME_STEP).values
        scaled = scaler.transform(last_days)
        X_test = np.reshape(scaled, (1, TIME_STEP, 1))
        pred_scaled = model.predict(X_test)
        pred = float(scaler.inverse_transform(pred_scaled)[0, 0])

        # Calculate simple confidence as inverse of standard deviation of last prices
        recent_std = np.std(last_days)
        confidence = max(0, min(100, 100 - (recent_std / pred * 100)))  # Scale to 0-100%

        return {"prediction": f"${pred:.2f}", "confidence": f"{confidence:.1f}%"}
    except Exception as e:
        return {"prediction": "N/A", "confidence": "N/A", "error": f"{e}"}


# --- ROUTES ---
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
    if not stock_symbol:
        return render_template('index.html', error="Please enter a stock symbol.")
    try:
        company_info = yf.Ticker(stock_symbol).info
        company_name = company_info.get('longName', stock_symbol)
    except: company_name = stock_symbol

    prediction = get_stock_prediction(stock_symbol)
    news = scrape_financial_news(stock_symbol)
    sentiment = get_sentiment(news)
    return render_template('result.html', symbol=stock_symbol, company_name=company_name, prediction=prediction, sentiment=sentiment)

# --- API ---
@app.route('/api/market-data')
def market_data():
    try:
        tickers = yf.Tickers(list(STOCKS_INFO.keys()))
        data = []
        for symbol, info in STOCKS_INFO.items():
            hist = tickers.tickers[symbol].history(period='2d')
            if len(hist) > 1:
                latest, prev = hist.iloc[-1], hist.iloc[-2]
                data.append({
                    "symbol": symbol,
                    "name": info["name"],
                    "logo": info["logo"],
                    "website": info["website"],
                    "price": float(latest['Close']),
                    "change": float(latest['Close'] - prev['Close']),
                    "changePercent": float((latest['Close'] - prev['Close']) / prev['Close'] * 100),
                    "dayHigh": float(latest['High']),
                    "dayLow": float(latest['Low']),
                    "volume": int(latest['Volume'])
                })
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/historical-data/<symbol>')
def get_historical_data(symbol):
    period = request.args.get('period', '1y')
    df = yf.Ticker(symbol).history(period=period)
    if len(df) < TIME_STEP:
        return jsonify({"dates": [], "prices": [], "error": f"Not enough data. Need {TIME_STEP} points."})
    df.index = df.index.strftime('%Y-%m-%d')
    prices = [float(p) if not np.isnan(p) else None for p in df['Close'].tolist()]
    return jsonify({"dates": list(df.index), "prices": prices})

@app.route('/api/predict-future/<symbol>')
def predict_future(symbol):
    model, scaler = get_model_and_scaler(symbol)
    if model is None or scaler is None:
        return jsonify({"dates": [], "prices": [], "error": "Model or scaler not found."}), 500

    df = yf.download(symbol, period="100d", interval="1d")
    if len(df) < TIME_STEP:
        return jsonify({"dates": [], "prices": [], "error": f"Not enough historical data. Need {TIME_STEP} points."}), 500

    last_days = df[['Close']].tail(TIME_STEP).values
    temp_input = list(scaler.transform(last_days))

    future_preds = []
    for _ in range(60):
        x_input = np.array(temp_input[-TIME_STEP:]).reshape((1, TIME_STEP, 1))
        yhat_scaled = model.predict(x_input, verbose=0)
        temp_input.append(yhat_scaled[0])
        pred = scaler.inverse_transform(yhat_scaled)[0, 0]
        future_preds.append(float(pred) if not np.isnan(pred) else None)

    today = datetime.now()
    dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 61)]
    return jsonify({"dates": dates, "prices": future_preds})

@app.route('/api/news/<symbol>')
def get_news(symbol):
    company_name = STOCKS_INFO.get(symbol.upper(), {}).get('name', symbol)
    query = f'("{company_name}" OR "{symbol}")'
    url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&q={urllib.parse.quote(query)}&language=en&category=business,technology"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        return jsonify(data.get('results', []))
    except Exception as e:
        return jsonify({"error": f"Failed to fetch news: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
