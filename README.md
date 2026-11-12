# movie-explorer

A Python command-line app that searches movies and shows details using the TMDB REST API.

## Run it
1. pip install requests
2. Set your TMDB read access token: export TMDB_READ_ACCESS_TOKEN="your-token"
3. python movie_explorer.py "inception"

## What it does
- Sends authenticated GET requests to the TMDB API
- Parses JSON responses and handles API errors
- Prints the top matches and details for the best result

This product uses the TMDB API but is not endorsed or certified by TMDB.
