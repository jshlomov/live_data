import os

from dotenv import load_dotenv

from app.api.groq_api import classify_news_message, extract_location_details
from app.api.news_api import fetch_news
from app.kafka_settings.admin import init_topics
from app.kafka_settings.producer import produce_message
from app.utils.location_util import get_lan_and_lon

load_dotenv(verbose=True)

if __name__ == '__main__':
    # init_topics()
    news_res = fetch_news()

    for news in news_res.get("articles", {}).get("results", []):
        article_type = classify_news_message(news["body"])
        location = extract_location_details(news.get("title"), news.get("body"))
        if not location:
            continue
        cords = get_lan_and_lon(location["country"], location["city"])
        if not cords or not cords[0] or not cords[1]:
            continue
        res_json = {
            "title": news["title"],
            "date": news["dateTime"],
            "type": article_type,
            "location": {
                "city": location["city"],
                "country": location["country"],
                "region": location["region"],
                "latitude": cords[0],
                "longitude": cords[1],
            },
            "body": news["body"],
        }

        print(res_json)
        listOfNews = []
        if res_json:
            listOfNews.append(res_json)
        if len(listOfNews) == 3:
            produce_message(os.environ.get("[TOPIC_NEWS_NAME]") , {"news": listOfNews}, "news")

    if listOfNews:
        produce_message(os.environ.get("TOPIC_NEWS_NAME") , {"news": listOfNews}, "news")

