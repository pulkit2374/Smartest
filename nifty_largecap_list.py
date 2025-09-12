import csv

def get_largecap_list():
    tickers = []
    try:
        with open("nse_largecap.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                tickers.append(row["Ticker"])
    except Exception as e:
        print(f"Error loading large cap list: {e}")
    return tickers
