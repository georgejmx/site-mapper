from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
import logging

from .routes import router
from .classify import site_to_matrix


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handler to initialise model upon server startup by calling it for first time"""
    site_to_matrix("Init")
    logging.info("Model initialised")
    yield


load_dotenv()
app = FastAPI(
    title="Site Mapper",
    summary="Classify websites into relative sentiment similarity",
    lifespan=lifespan,
)
app.include_router(router)


@app.get("/health", response_class=PlainTextResponse)
def health_controller():
    logging.info("Call to /health")
    return "Healthy"
