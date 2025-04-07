import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

def get_nse500_symbols():
    url = 'https://archives.nseindia.com/content/indices/ind_nifty500list.csv'
    df = pd.read_csv(url)
    return df['Symbol'].apply(lambda x: x + '.NS').tolist()

def calculate_trade_signal(symbol):
    try:
        data = yf.download(symbol, period='5d', interval='15m', progress=False)
        if len(data) < 20:
            return None

        latest = data.iloc[-1]
        previous = data.iloc[-2]
        high_breakout = latest['Close'] > max(data['High'][-10:-1])
        trend = latest['Close'] > data['Close'].rolling(window=10).mean().iloc[-1]
        volume_surge = latest['Volume'] > data['Volume'].rolling(window=10).mean().iloc[-1] * 1.5

        conditions = [high_breakout, trend, volume_surge]
        score = sum(conditions)
        confidence = int((score / len(conditions)) * 100)

        if score >= 2:
            return {
                'symbol': symbol,
                'entry': round(latest['Close'], 2),
                'target': round(latest['Close'] + 20, 2),
                'stop_loss': round(latest['Close'] - 5, 2),
                'confidence': f"{confidence}%",
                'reasons': [
                    "Breakout" if high_breakout else "",
                    "Trend Up" if trend else "",
                    "Volume Surge" if volume_surge else ""
                ]
            }
    except:
        return None

def scan_market():
    india = pytz.timezone('Asia/Kolkata')
    now = datetime.now(india)
    if now.hour < 9 or now.hour >= 15:
        return "Market Closed"

    nse500 = get_nse500_symbols()
    for symbol in nse500:
        result = calculate_trade_signal(symbol)
        if result:
            return result
    return None
