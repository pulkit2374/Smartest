# fetch_data.py

import yfinance as yf
from datetime import datetime, timedelta

def fetch_stock_data(ticker):
    try:
        #  Normalize to NSE ticker
        ticker = ticker.strip().upper()
        if not ticker.endswith(".NS"):
            ticker += ".NS"

        stock = yf.Ticker(ticker)
        info = stock.info

        name = info.get('longName', 'N/A')
        sector = info.get('sector', 'N/A')
        market_cap = info.get('marketCap', 'N/A')
        pe_ratio = info.get('trailingPE', 'N/A')
        pb_ratio = info.get('priceToBook', 'N/A')
        live_price = info.get('currentPrice', 0)  # or 'regularMarketPrice'

        # Historical returns
        end_date = datetime.today()
        start_5y = end_date - timedelta(days=5*365)
        start_3y = end_date - timedelta(days=3*365)
        start_1y = end_date - timedelta(days=365)

        hist_5y = stock.history(start=start_5y, end=end_date)
        hist_3y = stock.history(start=start_3y, end=end_date)
        hist_1y = stock.history(start=start_1y, end=end_date)

        def calc_return(hist):
            if hist.empty:
                return 'N/A'
            start_price = hist['Close'].iloc[0]
            end_price = hist['Close'].iloc[-1]
            return round(((end_price - start_price) / start_price) * 100, 2)

        return {
            "name": name,
            "sector": sector,
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "pb_ratio": pb_ratio,
            "live_price": live_price,
            "return_1y": calc_return(hist_1y),
            "return_3y": calc_return(hist_3y),
            "return_5y": calc_return(hist_5y)
        }

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None



def get_price_history(ticker):
    try:
        data = yf.download(ticker, period="1y", interval="1d")
        if data.empty:
            return {"dates": [], "prices": []}
        
        dates = [d.strftime("%Y-%m-%d") for d in data.index]
        prices = data["Close"].fillna(method="ffill").tolist()
        
        return {"dates": dates, "prices": prices}
    except Exception as e:
        print(f"Error fetching price history: {e}")
        return {"dates": [], "prices": []}
