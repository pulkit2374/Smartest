# refresh_largecap_data.py

import csv
import json
from fetch_data import fetch_stock_data
from score_stock import score_stock

from datetime import datetime
from time import sleep

INPUT_CSV = "nse_largecap.csv"
OUTPUT_CSV = "largecap_scored.csv"

def refresh_largecap_data():
    scored_data = []

    with open(INPUT_CSV, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        tickers = [row for row in reader]

    total = len(tickers)
    print(f"\nRefreshing data for {total} NSE Large Cap stocks...")

    for idx, stock in enumerate(tickers, 1):
        ticker = stock['Ticker']
        name = stock['Name']
        sector = stock['Sector']

        data = fetch_stock_data(ticker)
        if data:
            score, _ = score_stock(data)
            pe = data.get('pe_ratio', 0)
            return_1y = data.get('return_1y', 0)

            scored_data.append({
                "Ticker": ticker,
                "Name": name,
                "Sector": sector,
                "Score": score,
                "PE": pe,
                "Return_1Y": return_1y,
                "Updated_On": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        print(f"[{idx}/{total}] Processed {ticker}")
        sleep(0.5)  # polite delay to avoid rate limits

    # Write to CSV
    with open(OUTPUT_CSV, "w", newline='', encoding="utf-8") as file:
        fieldnames = ["Ticker", "Name", "Sector", "Score", "PE", "Return_1Y", "Updated_On"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scored_data)

    print(f"\n✅ Large cap data refreshed and saved to {OUTPUT_CSV}.")

if __name__ == "__main__":
    refresh_largecap_data()
