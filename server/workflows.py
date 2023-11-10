import logging

from .classify import site_to_matrix, find_site_similarity
from .scrape import scrape_site, clean_output
from .mongo import MongoConnection


def sketch_site(url: str) -> list[list[int]]:
    """
    Triggers the full pipeline of scraping a site, then generating a sentiment
    tensor representation to be used for measuring the relative emotional
    similarity of sites
    """
    logging.info("Sketch pipeline started")
    contents = scrape_site(url)
    cleaned_contents = clean_output(contents)
    logging.info(f"Site with url {url} scraped")

    sketch = site_to_matrix(cleaned_contents)
    logging.info("Prediction generated using model")
    
    connection = MongoConnection()
    sketch_id = connection.insert_sketch(url, sketch)
    del connection
    logging.info(f"Site data inserted into mongo with id: {sketch_id}")


def get_sites() -> list[str]:
    """Retrieves all sites present in mongo"""
    connection = MongoConnection()
    sketches = connection.get_sketches()
    del connection
    logging.info("Sketches retrieved")
    return [sketch["url"] for sketch in sketches]


def get_similarity_to(pivot_url: str) -> list[tuple[str, int]]:
    """Retrieves a list of sites ranked by similarity to provided site"""
    connection = MongoConnection()
    sketches = connection.get_sketches()
    del connection
    logging.info("Sketches retrieved")
    
    pivot_matrix = [
        sketch["sketch"] for sketch in sketches if sketch["url"] == pivot_url
    ][0]

    results = []
    for sketch in sketches:
        if sketch["url"] != pivot_url:
            results.append(
                (sketch["url"], find_site_similarity(pivot_matrix, sketch["sketch"]))
            )
    return results
