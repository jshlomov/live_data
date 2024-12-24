import json
import os
from tabnanny import check

from groq import Groq
from dotenv import load_dotenv

load_dotenv(verbose=True)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def classify_news_message(news_text):
    try:
        prompt = (
            f"""
            Classify the message in one of following categories:
            1. General News
            2. Historical Terrorism Event
            3. Current Terrorism Event

            News Message:
            "{news_text}"

            get just category number (1, 2, or 3) as response.
            """
        )
        completion_response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        category = completion_response.choices[0].message.content.strip()
        if category not in ["1", "2", "3"]:
            raise ValueError(f"Invalid category: {category}")
        if category == "1":
            category_name = "General News"
        elif category == "2":
            category_name = "Historical Terrorism Event"
        elif category == "3":
            category_name = "Current Terrorism Event"
        else:
            category_name = None
        return category_name

    except Exception as error:
        print(f"Classification error: {error}")
        return None


def extract_location_details(article_title, article_body):
    query = (
        f"""
        Extract the location details (City, Country, Region) from the following news article.
        If no specific city, country, or region is mentioned, return None for the missing fields.
        if u recognize the region by city and country, fill the region as you see.
        Respond in this exact JSON format:
        {{
            "city": ["city" or "null"],
            "country": ["country" or "null"],
             "region": ["region" or "null"]
        }}
        only one result for each and no additional comments at all
        and please dont use None!!

        News Message:
        "{
        article_title.replace("\\", ""),
        article_body.replace("\\", "") if article_body else ""
        }"
        """
    )

    try:
        completion_response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model="llama3-8b-8192",
        )

        result = json.loads(completion_response.choices[0].message.content)

        # return result
        if check_result(result):
            return result
        else:
            print(f"Validation failed for location details: {result}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def check_result(result):
    if not isinstance(result, dict):
        return False
    for key in {"city", "country", "region"}:
        if key not in result or (result[key] != "null" and not isinstance(result[key], str)):
            return False
    return True
