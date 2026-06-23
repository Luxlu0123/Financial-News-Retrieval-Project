import requests
import pandas as pd
import os
from datetime import datetime, timedelta

# Get data from Alpha Vantage API
API_KEY = "UUVDLET0E6UCKONO"
DEFAULT_TOPIC = "financial_markets"
DEFAULT_DAYS_BACK = 7


def fetch_articles(topic: str = DEFAULT_TOPIC, days_back: int = DEFAULT_DAYS_BACK, limit: int = 1000, csv_path: str = "financial_news_articles.csv") -> pd.DataFrame:
    """Fetch news articles from Alpha Vantage NEWS_SENTIMENT and save to CSV.

    Returns the dataframe of articles.
    """
    time_to = datetime.now()
    time_from = time_to - timedelta(days=days_back)

    time_from_str = time_from.strftime("%Y%m%dT%H%M")
    time_to_str = time_to.strftime("%Y%m%dT%H%M")

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "topics": topic,
        "time_from": time_from_str,
        "time_to": time_to_str,
        "limit": limit,
        "apikey": API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    articles = data.get("feed", [])

    rows = []
    for item in articles:
        rows.append(
            {
                "title": item.get("title"),
                "source": item.get("source"),
                "time_published": item.get("time_published"),
                "summary": item.get("summary"),
                "url": item.get("url"),
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print("Time range:", time_from_str, "to", time_to_str)
    print("Total articles:", len(df))
    print("Saved to:", os.path.abspath(csv_path))

    return df


if __name__ == "__main__":
    fetch_articles()