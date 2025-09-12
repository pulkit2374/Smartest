# advanced_factors.py

import yfinance as yf

def fetch_advanced_factors(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # PEG Ratio
        peg_ratio = info.get('pegRatio', 'N/A')
        if peg_ratio is None:
            peg_ratio = 'N/A'

        # Dividend Yield
        dividend_yield = info.get('dividendYield', 'N/A')
        if dividend_yield is not None and dividend_yield != 'N/A':
            dividend_yield = round(dividend_yield * 100, 2)
        else:
            dividend_yield = 'N/A'

        # 200 DMA Comparison
        hist = stock.history(period="200d")
        if not hist.empty:
            price_200dma = hist['Close'].mean()
            current_price = hist['Close'].iloc[-1]
            above_200dma = current_price > price_200dma
        else:
            above_200dma = 'N/A'

        return {
            "peg_ratio": peg_ratio,
            "dividend_yield": dividend_yield,
            "above_200dma": above_200dma
        }
    except Exception as e:
        print(f"Error fetching advanced factors for {ticker}: {e}")
        return {
            "peg_ratio": 'N/A',
            "dividend_yield": 'N/A',
            "above_200dma": 'N/A'
        }
