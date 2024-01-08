from math import floor
from dataclasses import dataclass
from fastapi import BackgroundTasks, APIRouter, HTTPException, status
import logging

from .workflows import sketch_site, get_sites, get_similarity_to

MAX_WORKERS = 5

router = APIRouter(prefix="/api")


@dataclass
class SketchRequest:
    urls: list[str]


@router.post("/sketch", status_code=status.HTTP_202_ACCEPTED)
async def sketch_controller(req: SketchRequest, tasks: BackgroundTasks) -> dict:
    """Route for scraping and profiling the urls provided"""
    if len(req.urls) > MAX_WORKERS:
        logging.info("Client error at /sketch")
        raise HTTPException(
            status_code=400,
            detail=f"Can process a max of {MAX_WORKERS} urls concurrently",
        )
    for url in req.urls:
        tasks.add_task(sketch_site, url)

    logging.info("Accepted call to /sketch")
    return {"message": "Sketching submitted"}


@router.get("/sites")
def sites_controller() -> dict:
    """Route for getting a list of all sites stored in mongo"""
    return {"sites": get_sites()}


@router.get("/similarity/{search_term}")
def similarity_controller(search_term: str) -> dict:
    """
    Route that retrieves a list of all sites by how similar their
    profile is to the site stipulated by the provided url snippet
    """
    pivot_url = None
    for url in get_sites():
        if search_term in url:
            pivot_url = url
            break

    if not pivot_url:
        logging.info("Client error at /similarity/:search_term")
        raise HTTPException(
            status_code=400, detail=f"{search_term} does not exist in application state"
        )
    results = get_similarity_to(pivot_url)
    output = {entry[0]: f"{floor(entry[1]*100)}%" for entry in results}
    logging.info(f"Successful call to /similarity/{search_term}")
    return {"similarity": output}
