from flask import Flask, render_template, request, redirect, url_for
from fetch_data import fetch_stock_data
from score_stock import score_stock
from market_today import get_market_snapshot, get_top_gainers_losers
from portfolio_tracker import read_portfolio, add_to_portfolio_web, delete_from_portfolio_web
from watchlist import Watchlist, read_watchlist, add_to_watchlist, delete_from_watchlist
from nifty_largecap_list import get_largecap_list
from filter_stocks import filter_stocks_web
from news_fetcher import fetch_news
from config import Config
from extension import db  
import yfinance as yf
import json

#  Initialize Flask and SQLAlchemy only once
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# After this, import your models
from portfolio_tracker import Portfolio
from watchlist import Watchlist


#  INR Formatter
def format_inr_crore(value):
    try:
        value = int(value) // 10_00_000
        s = str(value)[::-1]
        parts = [s[0:3]]
        s = s[3:]
        while s:
            parts.append(s[0:2])
            s = s[2:]
        return ','.join(parts)[::-1]
    except:
        return value

app.jinja_env.filters['inr_crore'] = format_inr_crore






# Route for the home page
@app.route('/')
def index():
    try:
        nifty, sensex = get_market_snapshot()
        # print("DEBUG: SENSEX RETURNED TO INDEX:", sensex) 
        top_gainers, top_losers = get_top_gainers_losers()
        portfolio_data = read_portfolio()  

        return render_template(
            'index.html',
            nifty=nifty,
            sensex=sensex,
            gainers=top_gainers,
            losers=top_losers,
            portfolio=portfolio_data 
        )    
    except Exception as e:
        print(f"[ERROR] Market Data Fetch Failed: {e}")
        return render_template("index.html", nifty=None, sensex=None, gainers=[], losers=[], portfolio=[])


# Route for searching stocks
from news_fetcher import fetch_news

import yfinance as yf
import json

@app.route('/search', methods=['GET', 'POST'])
def search():
    companies = get_largecap_list()
    data = None
    score = None
    breakdown = []
    news = []
    chart_labels = []
    chart_data = []

    if request.method == 'POST':
        ticker = request.form['ticker'].strip().upper()
        if not ticker.endswith('.NS'):
            ticker += '.NS'

        data = fetch_stock_data(ticker)
        if data:
            score, breakdown = score_stock(data, ticker)
            news = fetch_news(ticker)

            # 🎯 Fetch 1Y price data for chart
            hist = yf.Ticker(ticker).history(period="1y")
            chart_labels = hist.index.strftime("%Y-%m-%d").tolist()
            chart_data = hist["Close"].round(2).tolist()

    return render_template(
        'search.html',
        data=data,
        score=score,
        breakdown=breakdown,
        news=news,
        chart_labels=json.dumps(chart_labels),
        chart_data=json.dumps(chart_data)
    )


# Route for viewing portfolio

@app.route('/portfolio')
def portfolio():
    raw_portfolio = read_portfolio()
    enriched_portfolio = []
    total_invested = 0
    total_value = 0

    for stock in raw_portfolio:
        ticker = stock.ticker         
        quantity = stock.quantity
        buy_price = stock.buy_price


        data = fetch_stock_data(ticker)
        if not data:
            continue

        live_price = data.get('live_price', 0)
        gain_amount = round((live_price - buy_price) * quantity, 2)
        gain_percent = round(((live_price - buy_price) / buy_price) * 100, 2)

        total_invested += quantity * buy_price
        total_value += quantity * live_price

        enriched_portfolio.append({
            "Ticker": ticker,
            "Quantity": quantity,
            "BuyPrice": buy_price,
            "LivePrice": live_price,
            "GainAmount": gain_amount,
            "GainPercent": gain_percent,
        })

    pnl = round(total_value - total_invested, 2)
    pnl_percent = round((pnl / total_invested) * 100, 2) if total_invested != 0 else 0


    scroll = len(enriched_portfolio) > 5

    return render_template("portfolio.html",
                           portfolio=enriched_portfolio,
                           invested=round(total_invested, 2),
                           value=round(total_value, 2),
                           pnl=pnl,
                           pnl_percent=pnl_percent,
                           scroll=scroll)



# Route for adding stock to the portfolio
@app.route('/add_portfolio', methods=['POST'])
def add_portfolio():
    try:
        ticker = request.form['ticker'].strip().upper()
        quantity = float(request.form['quantity'])
        buy_price = float(request.form['buy_price'])

        if not ticker.endswith('.NS'):
            ticker += '.NS'

        add_to_portfolio_web(ticker, quantity, buy_price)
        return redirect(url_for('portfolio'))
    except ValueError:
        return "❌ Invalid input! Please enter numeric values for quantity and buy price.", 400


@app.route('/delete_portfolio/<ticker>')
def delete_portfolio(ticker):
    delete_from_portfolio_web(ticker)
    return redirect(url_for('portfolio'))


# Route for viewing watchlist

@app.route('/watchlist')
def watchlist():
    watchlist_data = read_watchlist()
    enriched_watchlist = []

    for stock in watchlist_data:
        ticker = stock.ticker
        name = stock.name
        saved_on = stock.saved_on or 'N/A'


        data = fetch_stock_data(ticker)
        if not data:
            continue

        live_price = data.get('live_price', 0)
        score, _ = score_stock(data, ticker)

        enriched_watchlist.append({
            "ticker": ticker,
            "name": name,
            "saved_on": saved_on,
            "live_price": live_price,
            "score": score
        })

    return render_template("watchlist.html", watchlist=enriched_watchlist)


@app.route('/delete_watchlist/<ticker>')
def delete_watchlist(ticker):
    delete_from_watchlist(ticker)
    return redirect(url_for('watchlist'))



@app.route('/add_watchlist', methods=['POST'])
def add_watchlist():
    ticker = request.form['ticker']
    name = request.form['name']
    add_to_watchlist(ticker, name)
    return redirect(url_for('watchlist'))







@app.route('/filter', methods=['GET', 'POST'])
def filter():
    results = []
    if request.method == 'POST':
        min_score = request.form.get('min_score', type=float)
        min_return = request.form.get('min_return', type=float)
        pe_low = request.form.get('pe_low', type=float)
        pe_high = request.form.get('pe_high', type=float)
        sector_query = request.form.get('sector_query', '').strip()
        pe_range = (pe_low, pe_high) if pe_low is not None and pe_high is not None else None

        results = filter_stocks_web(min_score, min_return, pe_range, sector_query)

    return render_template('filter.html', results=results)






if __name__ == "__main__":
    from waitress import serve
    import os

    port = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)