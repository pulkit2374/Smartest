# filter_stocks.py

import csv
from tabulate import tabulate

def filter_stocks():
    scored_file = "largecap_scored.csv"

    try:
        with open(scored_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            stocks = [row for row in reader]
    except FileNotFoundError:
        print("\nPlease run your daily refresh (refresh_largecap_data.py) first to generate scored data.")
        return

    print("\n=== NSE Large Cap Filtering ===")

    min_score_input = input("Enter minimum score (press Enter to skip): ").strip()
    min_return_input = input("Enter minimum 1Y return % (press Enter to skip): ").strip()
    pe_range_input = input("Enter PE range (low-high, e.g., 10-25) or press Enter to skip: ").strip()

    filtered = []

    for stock in stocks:
        try:
            score = float(stock["Score"])
            return_1y = float(stock["Return_1Y"])
            pe = float(stock["PE"])
        except:
            continue

        if min_score_input:
            if score < float(min_score_input):
                continue

        if min_return_input:
            if return_1y < float(min_return_input):
                continue

        if pe_range_input:
            try:
                low, high = map(float, pe_range_input.split("-"))
                if not (low <= pe <= high):
                    continue
            except:
                print("Invalid PE range format. Skipping PE filter.")

        filtered.append({
            "Ticker": stock["Ticker"],
            "Name": stock["Name"],
            "Sector": stock["Sector"],
            "Score": score,
            "PE": pe,
            "Return_1Y": return_1y
        })

    if not filtered:
        print("\nNo stocks matched your filters.")
        return

    filtered.sort(key=lambda x: x["Score"], reverse=True)
    top_stocks = filtered[:10]

    table_data = []
    for idx, stock in enumerate(top_stocks, 1):
        table_data.append([
            idx,
            stock["Ticker"],
            stock["Name"],
            stock["Sector"],
            stock["Score"],
            stock["PE"],
            f"{stock['Return_1Y']}%"
        ])

    headers = ["Rank", "Ticker", "Name", "Sector", "Score", "PE", "1Y Return"]
    print("\n===== Top Filtered Stocks =====")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    print("\nFiltering completed.")








def filter_stocks_web(min_score=None, min_return=None, pe_range=None, sector_query=None):
    scored_file = "largecap_scored.csv"
    try:
        with open(scored_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            stocks = [row for row in reader]
    except FileNotFoundError:
        return []

    filtered = []
    for stock in stocks:
        try:
            score = float(stock["Score"])
            return_1y = float(stock["Return_1Y"])
            pe = float(stock["PE"])
            sector = stock.get("Sector", "").lower()
        except:
            continue

        if min_score and score < min_score:
            continue
        if min_return and return_1y < min_return:
            continue
        if pe_range:
            try:
                low, high = pe_range
                if not (low <= pe <= high):
                    continue
            except:
                continue
        if sector_query:
            if sector_query.lower() not in sector:
                continue

        filtered.append({
            "Ticker": stock["Ticker"],
            "Name": stock["Name"],
            "Sector": stock["Sector"],
            "Score": score,
            "PE": pe,
            "Return_1Y": return_1y
        })

    return sorted(filtered, key=lambda x: x["Score"], reverse=True)
