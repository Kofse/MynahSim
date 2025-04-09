from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time

CACHE_DIR = Path("web_cache")
CACHE_DIR.mkdir(exist_ok=True)

def duckduckgo_search(query: str, max_results: int = 3) -> list:
    with DDGS() as ddgs:
        return [{"title": r["title"], "link": r["href"]} for r in ddgs.text(query, max_results=max_results)]

def scrape_website(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for element in soup(["script", "style", "nav", "footer"]):
            element.decompose()
        return soup.get_text(separator="\n", strip=True)[:5000]
    except Exception as e:
        return f"Error: {str(e)}"

def clean_old_cache(days: int = 7):
    now = time.time()
    for file in CACHE_DIR.glob("*"):
        if file.is_file() and (now - file.stat().st_mtime) > (days * 86400):
            file.unlink()
