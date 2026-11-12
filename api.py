import logging
import os
import time

import requests
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import APIKeyHeader

import movie_explorer

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("movie_api")

app = FastAPI(title="Movie Explorer API", description="Small API wrapping TMDB movie search")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(key: str = Depends(api_key_header)):
    """Reject requests that don't send the correct X-API-Key header."""
    expected = os.environ.get("MOVIE_API_KEY")
    if not expected:
        raise HTTPException(status_code=500, detail="Server API key not configured")
    if key != expected:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log method, path, status code, and response time for every request."""
    start = time.time()
    response = await call_next(request)
    ms = (time.time() - start) * 1000
    logger.info("%s %s -> %s (%.0f ms)", request.method, request.url.path, response.status_code, ms)
    return response


@app.get("/search", dependencies=[Depends(require_api_key)])
def search(title: str):
    """Search movies by title."""
    try:
        results = movie_explorer.search_movies(title)
    except requests.exceptions.HTTPError as err:
        raise HTTPException(status_code=502, detail=f"Upstream API error: {err}")
    return [
        {"id": m["id"], "title": m["title"], "release_date": m.get("release_date")}
        for m in results[:5]
    ]


@app.get("/movie/{movie_id}", dependencies=[Depends(require_api_key)])
def movie(movie_id: int):
    """Get details for one movie by its TMDB id."""
    try:
        return movie_explorer.get_movie_details(movie_id)
    except requests.exceptions.HTTPError as err:
        raise HTTPException(status_code=502, detail=f"Upstream API error: {err}")
