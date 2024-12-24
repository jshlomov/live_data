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
            return the category only without the number            
            1. general news
            2. terrorism event history
            3. terrorism event now
            
            text:
            "{news_text}"
            """
        )
        completion_response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )

        category = completion_response.choices[0].message.content.strip()
        if category not in ["general news", "terrorism event history", "terrorism event now"]:
            raise ValueError(f"Invalid category: {category}")
        return category

    except Exception as error:
        print(f"Classification error: {error}")
        return None


def extract_location_details(article_title, article_body):
    query = (
        f"""
        Extract the location details (City, Country, Region) from the following news article. If no specific city, country,
        or region is mentioned, return None for the missing fields. if u recognize the region by city and country,
        fill the region as you see. only one result for each and no additional comments at all and please dont use None!!
        Respond in this exact JSON format:
        {{ "city": ["city" or "null"], "country": ["country" or "null"], "region": ["region" or "null"] }}

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

        if not result or not isinstance(result, dict) or "city" not in result or "country" not in result or "region" not in result:
            raise ValueError("Invalid JSON response")

        if result["city"] == "null" and result["country"] == "null" and result["region"] == "null":
            raise ValueError("Invalid JSON response")

        return result

    except Exception as e:
        print(f"Error: {e}")
        return None
