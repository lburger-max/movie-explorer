import os
import sys
import requests

BASE_URL = "https://api.themoviedb.org/3"


def get_headers():
    token = os.environ.get("TMDB_READ_ACCESS_TOKEN")
    if not token:
        sys.exit("Set the TMDB_READ_ACCESS_TOKEN environment variable first.")
    return {"Authorization": f"Bearer {token}", "accept": "application/json"}


def search_movies(title):
    """Search for movies by title and return a list of results (parsed JSON)."""
    response = requests.get(
        f"{BASE_URL}/search/movie",
        headers=get_headers(),
        params={"query": title},
        timeout=10,
    )
    response.raise_for_status()  # raises an error on 401, 404, 429, etc.
    return response.json()["results"]


def get_movie_details(movie_id):
    """Fetch full details for one movie by its TMDB id."""
    response = requests.get(
        f"{BASE_URL}/movie/{movie_id}",
        headers=get_headers(),
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python movie_explorer.py 'movie title'")
    title = " ".join(sys.argv[1:])
    try:
        results = search_movies(title)
    except requests.exceptions.HTTPError as err:
        sys.exit(f"API error: {err}")
    if not results:
        sys.exit("No movies found.")
    for movie in results[:5]:
        print(f"{movie['title']} ({movie.get('release_date', 'n/a')[:4]})")
    top = get_movie_details(results[0]["id"])
    print(f"\nTop result: {top['title']}, {top.get('runtime')} min")
    print(top.get("overview", ""))


if __name__ == "__main__":
    main()
