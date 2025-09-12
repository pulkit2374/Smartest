def fetch_news(company_name):
    try:
        query = company_name.replace(" ", "%20")
        url = f"https://finance.yahoo.com/quote/{query}/news?p={query}"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all('li', {'class': 'js-stream-content'})

        news_items = []
        today = datetime.now()
        week_ago = today - timedelta(days=7)

        for article in articles:
            try:
                headline_tag = article.find('h3')
                if not headline_tag:
                    continue
                title = headline_tag.get_text(strip=True)
                link_tag = headline_tag.find('a')
                url = "https://finance.yahoo.com" + link_tag['href'] if link_tag else "#"

                time_tag = article.find('time')
                if time_tag and time_tag.has_attr('datetime'):
                    published_date = datetime.strptime(time_tag['datetime'][:10], "%Y-%m-%d")
                else:
                    continue

                if published_date < week_ago:
                    continue

                sentiment = classify_sentiment(title)

                news_items.append({
                    "date": published_date.strftime("%Y-%m-%d"),
                    "title": title,
                    "url": url,
                    "sentiment": sentiment
                })

                if len(news_items) >= 5:
                    break

            except Exception:
                continue

        return news_items

    except Exception:
        return []
