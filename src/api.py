import asyncpraw
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET
from io import BytesIO
import requests
from random import randint

reddit = asyncpraw.Reddit (
    client_id = REDDIT_CLIENT_ID,
    client_secret = REDDIT_CLIENT_SECRET,
    user_agent = "default_bot 2.0 by default_user"
)

def get_cat(type: str) -> tuple[BytesIO, str] | tuple[None, None]:
    """Fetches a cat image or gif and returns a (BytesIO, filename) tuple."""
    if type == "gif":
        url = "https://cataas.com/cat/gif"
        filename = "cat.gif"
    elif type == "img":
        url = "https://cataas.com/cat"
        filename = "cat.jpg"
    else:  # type == "random"
        if randint(0, 1):
            url = "https://cataas.com/cat/gif"
            filename = "cat.gif"
        else:
            url = "https://cataas.com/cat"
            filename = "cat.jpg"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BytesIO(response.content), filename
    except Exception as e:
        print(f"Error fetching cat: {e}")

    return None, None

def get_trivia():
    """Returns a random trivia"""
    response = requests.get("https://opentdb.com/api.php?amount=1&category=9&difficulty=easy&type=multiple")
    if response.status_code == 200:
        data = response.json()
        one_result = data["results"][0]
        return one_result
