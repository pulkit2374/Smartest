

# **SMARTEST – Stock Market Analysis, Ranking & Evaluation Tool**

🔗 **Live Demo:** [https://smartest-pm.up.railway.app/]

A full-stack web application to analyze and rank Indian NSE stocks using a **10-point smart scoring system**, helping users make informed investment decisions and manage portfolios.

---

## **Demo**

<img width="1903" height="961" alt="Smartest_1" src="https://github.com/user-attachments/assets/990493bd-fdd1-4712-a899-df3da8fd7a7f" />

<img width="1909" height="968" alt="Smartest_2" src="https://github.com/user-attachments/assets/9e6b1c06-52a9-4b98-ac34-b57abb56dc8b" />


---

## **Features**

* **Search NSE top 500 stocks** with ticker autocomplete.
* **Smart 10-point scoring system** evaluating profitability, growth, valuation, risk, promoter stake, and momentum.
* **Portfolio & watchlist management** with persistent **MySQL storage**.
* **Charts & visualization**: 1-year stock prices via Chart.js.
* **News & sentiment analysis**: fetch latest stock news.
* **Filter stocks** by score, sector, and valuation.
* **Duplicate handling** in portfolio and watchlist.
* Planned deployment on **Render / Railway**.

---

## **Tech Stack**

* **Backend:** Python, Flask, SQLAlchemy, MySQL
* **Frontend:** HTML, Bootstrap 5, Jinja2, Chart.js
* **Data Sources:** yfinance, Yahoo News API
* **Tools:** VS Code

---

## **Usage**

1. Search for a stock using the input field (autocomplete available).
2. View the **smart score** and stock details.
3. Add stocks to **portfolio or watchlist** (data stored in MySQL).
4. View **1-year price charts** and **latest news**.
5. Filter stocks by **score, sector, and valuation**.

---

## **Project Structure**

```
SMARTEST/
├── app.py                  ← main Flask app
├── watchlist.py            ← MySQL watchlist logic
├── portfolio_tracker.py    ← Portfolio management
├── config.py               ← MySQL credentials
├── extension.py            ← Shared DB instance
├── fetch_data.py
├── score_stock.py
├── filter_stocks.py
├── nifty_largecap.csv      ← Top 500 NSE stocks
├── templates/
│   ├── index.html
│   ├── watchlist.html
│   └── search.html
└── static/
    └── style.css
```

---

## **Key Learnings / Skills Gained**

* **Full-stack web development** with Python Flask and Bootstrap.
* **Database integration** using MySQL and SQLAlchemy.
* **API integration** for stock prices and news.
* **Data visualization** using Chart.js.
* **Modular code architecture** for scalability and easy maintenance.

---

If you want, I can **also add a short “Planned Future Enhancements” section** to make it look even more professional on GitHub. Do you want me to add that?
