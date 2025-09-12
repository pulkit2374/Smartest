import requests
import yfinance as yf
import json
import os

CACHE_FILE = "gainers_losers.json"

def get_nifty_data():
    url = "https://www.nseindia.com/api/marketStatus"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)
    response = session.get(url, headers=headers)
    data = response.json()

    for idx in data['marketState']:
        if idx['index'] == 'NIFTY 50':
            return {
                "index": idx['index'],
                "last": idx['last'],
                "variation": idx['variation'],
                "percentChange": idx['percentChange']
            }
    return None



def get_sensex_data():
    try:
        index = "^BSESN"  # BSE SENSEX index symbol on Yahoo Finance
        stock = yf.Ticker(index)
        hist = stock.history(period="2d")  # 2 days needed to calculate % change

        if len(hist) < 2:
            return None

        last = hist['Close'].iloc[-1]
        prev = hist['Close'].iloc[-2]
        change = last - prev
        percent = (change / prev) * 100

        return {
            "index": "SENSEX",
            "last": round(last, 2),
            "variation": round(change, 2),
            "percentChange": round(percent, 2)
        }

    except Exception as e:
        print("Error fetching SENSEX via yfinance:", e)
        return None




def get_top_gainers_losers():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/"
    }

    session = requests.Session()
    session.headers.update(headers)

    # 1️⃣ Try NSE Official API
    try:
        session.get("https://www.nseindia.com", timeout=5)

        gainers_url = "https://www.nseindia.com/api/live-analysis-variations?index=gainers"
        losers_url = "https://www.nseindia.com/api/live-analysis-variations?index=losers"

        gainers_resp = session.get(gainers_url, timeout=5)
        losers_resp = session.get(losers_url, timeout=5)

        gainers_data = gainers_resp.json()
        losers_data = losers_resp.json()

        top_gainers = [f"{g['symbol']} ({g['pChange']}%)" for g in gainers_data["data"][:5]]
        top_losers = [f"{l['symbol']} ({l['pChange']}%)" for l in losers_data["data"][:5]]

        # Save to cache
        with open(CACHE_FILE, "w") as f:
            json.dump({"gainers": top_gainers, "losers": top_losers}, f, indent=2)

        return top_gainers, top_losers

    except Exception as e:
        print("⚠️ NSE API failed:", e)

    # 2️⃣ Try TickerTape Unofficial API
    try:
        gainers_resp = requests.get("https://api.tickertape.in/stocks/equity/gainers-losers?type=gainers", timeout=5)
        losers_resp = requests.get("https://api.tickertape.in/stocks/equity/gainers-losers?type=losers", timeout=5)

        gainers_data = gainers_resp.json().get("data", [])[:5]
        losers_data = losers_resp.json().get("data", [])[:5]

        top_gainers = [f"{g['ticker']} ({g['change']}%)" for g in gainers_data]
        top_losers = [f"{l['ticker']} ({l['change']}%)" for l in losers_data]

        return top_gainers, top_losers

    except Exception as e:
        print("⚠️ TickerTape API failed:", e)

    # 3️⃣ Try fallback cache (from previous successful runs)
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cached = json.load(f)
                return cached.get("gainers", []), cached.get("losers", [])
        except:
            pass

    # 4️⃣ Try local sample file
    try:
        with open("gainers_losers_sample.json", "r") as f:
            sample = json.load(f)
            gainers = [f"(Sample) {g}" for g in sample.get("gainers", [])]
            losers = [f"(Sample) {l}" for l in sample.get("losers", [])]
            return gainers, losers
    except Exception as e:
        print("⚠️ Sample fallback failed:", e)
        return ["⚠️ Gainers data unavailable"], ["⚠️ Losers data unavailable"]








def get_market_snapshot():
    try:
        nifty = get_nifty_data()
        sensex = get_sensex_data()

        
        print("DEBUG - NIFTY:", nifty)
        print("DEBUG - SENSEX:", sensex)

        return nifty, sensex
    except Exception as e:
        print(f"Error fetching market snapshot: {e}")
        return None, None
