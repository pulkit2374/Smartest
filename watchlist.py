from datetime import datetime
from flask import current_app
from extension import db  # ✅ Use shared db instance
import yfinance as yf

class Watchlist(db.Model):
    __tablename__ = 'watchlist'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    saved_on = db.Column(db.DateTime, default=datetime.utcnow)
    saved_price = db.Column(db.Float)
    score = db.Column(db.Float)

    def __repr__(self):
        return f"<{self.ticker} - {self.name} - {self.saved_price}>"

def read_watchlist():
    return Watchlist.query.all()

def add_to_watchlist(ticker, name, score=None):
    ticker = ticker.strip().upper()
    if not ticker.endswith(".NS"):
        ticker += ".NS"

    existing = Watchlist.query.filter_by(ticker=ticker).first()
    if existing:
        print(f"{ticker} already in watchlist.")
        return

    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get("currentPrice", 0)
    except:
        price = 0

    entry = Watchlist(
        ticker=ticker,
        name=name,
        saved_price=price,
        score=score
    )
    db.session.add(entry)
    db.session.commit()
    print(f"{ticker} added to watchlist.")

def delete_from_watchlist(ticker):
    stock = Watchlist.query.filter_by(ticker=ticker).first()
    if stock:
        db.session.delete(stock)
        db.session.commit()
        print(f"{ticker} removed from watchlist.")
