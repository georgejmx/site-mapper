from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from fastapi import BackgroundTasks, APIRouter, HTTPException, status
import logging

from .workflows import sketch_site, get_sites

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
            detail=f"Can process a max of {MAX_WORKERS} urls concurrently"
        )
    for url in req.urls:
        tasks.add_task(sketch_site, url)
    
    logging.info("Accepted call to /sketch")
    return {"message": "Sketching submitted"}


@router.get("/sites")
def sites_controller() -> dict:
    """Route for getting a list of all sites stored in mongo"""
    return {"sites": get_sites()}


# @router.get("/similarity/{url}")
# def similarity_controller(url: str) -> list[str]:
#     """
#     Route that retrieves an ordered list of all sites by how similar their
#     profile is to the site stipulated by the provided url
#     """
