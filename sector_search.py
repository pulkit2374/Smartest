# sector_search.py (tabulate integrated)

import csv
from fetch_data import fetch_stock_data
from score_stock import score_stock
from tabulate import tabulate

def load_sector_stocks(sector_name, csv_file="nifty_stocks.csv"):
    tickers = []
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Sector'].strip().lower() == sector_name.strip().lower():
                tickers.append({
                    "ticker": row['Ticker'].strip(),
                    "name": row['Name'].strip(),
                    "sector": row['Sector'].strip()
                })
    return tickers

def search_stocks_by_sector():
    sector_name = input("\nEnter sector to search (e.g., Technology, Energy): ").strip()
    stocks = load_sector_stocks(sector_name)

    if not stocks:
        print(f"\nNo stocks found for sector '{sector_name}'. Check spelling or sector availability.")
        return

    scored_stocks = []
    print(f"\nFetching and scoring stocks in sector: {sector_name}...\n")

    for stock in stocks:
        data = fetch_stock_data(stock['ticker'])
        if data:
            score, _ = score_stock(data)
            scored_stocks.append({
                "rank": len(scored_stocks) + 1,
                "ticker": stock['ticker'],
                "name": stock['name'],
                "score": score
            })

    if not scored_stocks:
        print("\nNo data could be fetched for the selected sector.")
        return

    scored_stocks.sort(key=lambda x: x['score'], reverse=True)

    table_data = []
    for idx, stock in enumerate(scored_stocks, 1):
        table_data.append([idx, stock['ticker'], stock['name'], stock['score']])

    headers = ["Rank", "Ticker", "Name", "Score"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    print("\nSearch completed.")