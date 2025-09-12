# portfolio_tracker.py

from datetime import datetime
from extension import db  # ✅ shared db instance


# ─── Portfolio Table ───────────────────────────────────────
class Portfolio(db.Model):
    __tablename__ = 'portfolio'

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<{self.ticker} - Qty: {self.quantity} @ {self.buy_price}>"


# ─── Functions ──────────────────────────────────────────────

def read_portfolio():
    return Portfolio.query.all()

def add_to_portfolio_web(ticker, quantity, buy_price):
    ticker = ticker.strip().upper()
    if not ticker.endswith(".NS"):
        ticker += ".NS"

    existing = Portfolio.query.filter_by(ticker=ticker).first()
    if existing:
        print(f"{ticker} already in portfolio.")
        return

    stock = Portfolio(
        ticker=ticker,
        quantity=quantity,
        buy_price=buy_price
    )
    db.session.add(stock)
    db.session.commit()
    print(f"{ticker} added.")

def delete_from_portfolio_web(ticker):
    stock = Portfolio.query.filter_by(ticker=ticker).first()
    if stock:
        db.session.delete(stock)
        db.session.commit()
        print(f"{ticker} removed.")
