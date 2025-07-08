import random
import requests
from bs4 import BeautifulSoup
from logger import logging


def get_random_users_agents() -> str:
    """Returns a random user-agent string to mimic different browsers."""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    ]
    return random.choice(user_agents)

def get_page_content(url: str) -> str:
    headers = {'User-Agent': get_random_users_agents()}

    try:
        response = requests.get(url=url, headers=headers, timeout=10)
        response.raise_for_status()

        return response.text if response.text else ""
    except requests.exceptions.RequestException as e:
        logging.exception("Failed fetching %s", url, exc_info=e)
        return ""