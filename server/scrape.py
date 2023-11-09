import requests
from bs4 import BeautifulSoup
from io import StringIO

MAX_ENTRIES = 8000
TARGET_ELEMENTS = ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li"]


def scrape_site(url: str, is_recurse: bool = True) -> list[str]:
    """
    Scrapes a single site with the provided url. First scrapes the raw HTML
    content, then scrapes all local links from the landing page
    """
    contents = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    text_tags = [tag.text for tag in soup.find_all(TARGET_ELEMENTS)]
    for text in text_tags:
        if len(contents) >= MAX_ENTRIES:
            return contents
        contents.append(text.replace("\n", "").strip())

    if is_recurse:
        outgoing_links = [a["href"] for a in soup.find_all("a", href=True)]
        local_links = [link for link in outgoing_links if link.startswith("/")]
        for link in local_links:
            contents.extend(scrape_site(url + link, False))
    return contents


def clean_output(contents: list[str]) -> str:
    """Cleans and concatenates an array of scraped strings into a block"""
    builder = StringIO()
    for entry in contents:
        if len(entry.split()) >= 3:
            builder.write(entry)
            builder.write(". ")
    return builder.getvalue()
