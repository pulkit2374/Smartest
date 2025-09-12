from portfolio_tracker import db  # or from app import db

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text, nullable=True)
