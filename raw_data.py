import requests
import pandas as pd
import os
from datetime import datetime, timedelta

API_KEY = "UUVDLET0E6UCKONO"
url = "https://www.alphavantage.co/query"

TOPICS = [
    "financial_markets",
    "economy_fiscal",
    "economy_monetary",
    "finance",
    "economy_macro"
]

DAYS_BACK = 7

time_to = datetime.now()
time_from = time_to - timedelta(days=DAYS_BACK)

time_from_str = time_from.strftime("%Y%m%dT%H%M")
time_to_str = time_to.strftime("%Y%m%dT%H%M")

params = {
    "function": "NEWS_SENTIMENT",
    "topics": "financial_markets",
    "time_from": time_from_str,
    "time_to": time_to_str,
    "limit": 1000,
    "apikey": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

articles = data.get("feed", [])

rows = []

for item in articles:
    rows.append({
        "title": item.get("title"),
        "source": item.get("source"),
        "time_published": item.get("time_published"),
        "summary": item.get("summary"),
        "url": item.get("url")
    })

df = pd.DataFrame(rows)

csv_path = "financial_news_articles.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print("Time range:", time_from_str, "to", time_to_str)
print("Total articles:", len(df))
print("Saved to:", os.path.abspath(csv_path))