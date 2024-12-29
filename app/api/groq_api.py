import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv(verbose=True)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_news_message(news_text):
    try:
        query = (
            f"""
            i want you to classify this text. the options i want you to classify is:
            1. a general news as "general"
            2. a terrorism event that happen already (historical) as "history terror"
            3. a  terrorism event that happen now "actual terror"
            return the classification only.
            here is the text:
            "{news_text}"
            """
        )
        completion_response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model="llama3-8b-8192",
        )

        category = completion_response.choices[0].message.content.strip()
        if category not in ["general", "history terror", "actual terror"]:
            raise ValueError(f"Invalid category: {category}")
        return category

    except Exception as error:
        print(f"Classification error: {error}")
        return None


def extract_location_details(article_title, article_body):
    query = (
        f"""
        I want you to extract the location of the terrorist act. Extract the information from the text
        as (city, country, region). If you only see country and city you can fill in the region according to
        what you think is correct. If you don't have information for the values you don't have information
        for, return None.
        Another thing, I want you to return in json format in the form of {{city:..., country:.., region:..}}
        in one line.
        return the json only without any comments. no explanations, just the json.
        this is the text:
        "{
        article_title,
        article_body
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

        return result

    except Exception as e:
        print(f"Error: {e}")
        return None
