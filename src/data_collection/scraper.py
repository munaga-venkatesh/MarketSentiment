import random
import requests
from bs4 import BeautifulSoup
from src.logger import logging


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

def extract_body(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for scrit_or_style in soup(["scrit", "style"]):
        scrit_or_style.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]