import json
import os
import requests
from dotenv import load_dotenv

load_dotenv(verbose=True)

api_key = os.environ["NEWS_API_KEY"]

url = "https://eventregistry.org/api/v1/article/getArticles"
body = {
    "action": "getArticles",
    "keyword": "terror attack",
    "ignoreSourceGroupUri": "paywall/paywalled_sources",
    "articlesPage": 1,
    "articlesCount": 100,
    "articlesSortBy": "socialScore",
    "articlesSortByAsc": False,
    "dataType": ["news", "pr"],
    "forceMaxDataTimeWindow": 31,
    "resultType": "articles",
    "apiKey": api_key,
}


# def get_news():
#     response = requests.post(url, json=body)
#     json_response = response.json()
#     return json_response

def get_news():
    try:
        response = requests.post(url, json=body)
        response.raise_for_status()  # Raise an error for HTTP status codes >= 400
        return response.json()  # Attempt to parse JSON
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        raise
    except requests.exceptions.JSONDecodeError:
        print(f"Invalid JSON received: {response.text}")
        raise

def get_news_from_json(filename: str):
    with open(filename, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data

if __name__ == '__main__':
    news_res = get_news_from_json('../data/data.json')['articles']['results']
    print(news_res[0])

