# Movie Explorer

![Tests](https://github.com/lburger-max/movie-explorer/actions/workflows/tests.yml/badge.svg)

A Python project that searches movies using the [TMDB](https://www.themoviedb.org/) REST API. It includes a command-line tool and a small web API (built with FastAPI) that requires an API key, logs every request, and handles upstream errors.

I built this to practice working with REST APIs, JSON, authentication, testing, and a Git/GitHub workflow.

## Features

- **Command-line tool:** search for a movie and see the top matches plus details for the best result
- **Authenticated API calls:** sends a Bearer token to TMDB and keeps secrets in environment variables, never in code
- **Own web API:** `/search` and `/movie/{id}` endpoints built with FastAPI
- **API key protection:** requests to the API must include a valid `X-API-Key` header, or they are rejected with a 401
- **Request logging:** logs the method, path, status code, and response time of every request
- **Error handling:** upstream TMDB failures are returned as clear 502 responses instead of crashing
- **Automatic docs:** interactive documentation at `/docs`
- **Unit tests and CI:** tests mock the API, and GitHub Actions runs them on every push

## Project structure

```
movie-explorer/
├── movie_explorer.py        # TMDB client and command-line tool
├── api.py                   # FastAPI web service (auth, logging, endpoints)
├── test_movie_explorer.py   # unit tests (TMDB calls are mocked)
├── requirements.txt         # dependencies
└── .github/workflows/
    └── tests.yml            # GitHub Actions: runs pytest on every push
```

## Setup

You need Python 3.9+ and a free TMDB account.

1. **Get a TMDB token.** Create an account at themoviedb.org, then request an API key in your account's API settings. Copy the **API Read Access Token** (the long one).
2. **Clone and install:**
   ```bash
   git clone https://github.com/lburger-max/movie-explorer
   cd movie-explorer
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Set your token as an environment variable** (never put it in a file):
   ```bash
   export TMDB_READ_ACCESS_TOKEN="your-token-here"
   # Windows PowerShell: $env:TMDB_READ_ACCESS_TOKEN="your-token-here"
   ```

## Usage

### Command line

```bash
python movie_explorer.py "inception"
```

Prints up to five matching titles with release years, then the runtime and description of the top result.

### Web API

Create a key for your own API and start the server:

```bash
export MOVIE_API_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(16))')"
python -m uvicorn api:app --reload
```

Then open `http://127.0.0.1:8000/docs` for the interactive docs, or call the endpoints directly:

```bash
curl "http://127.0.0.1:8000/search?title=inception" -H "X-API-Key: $MOVIE_API_KEY"
curl "http://127.0.0.1:8000/movie/27205" -H "X-API-Key: $MOVIE_API_KEY"
```

| Endpoint | Description |
|---|---|
| `GET /search?title=...` | Search movies by title (top 5 results) |
| `GET /movie/{movie_id}` | Full details for one movie by its TMDB id |
| `GET /docs` | Auto-generated interactive documentation |

### Responses and errors

| Status | Meaning |
|---|---|
| 200 | Success |
| 401 | Missing or invalid `X-API-Key` |
| 500 | Server is missing `MOVIE_API_KEY` |
| 502 | TMDB returned an error (for example, an invalid TMDB token) |

### Logging

Every request is logged, for example:

```
2026-11-12 07:19:56 INFO GET /search -> 200 (312 ms)
```

## Tests

```bash
pytest
```

The tests mock the TMDB API, so no real token is needed. GitHub Actions runs them automatically on every push and pull request.

## How authentication works

- **Outbound:** this app authenticates to TMDB with a Bearer token read from `TMDB_READ_ACCESS_TOKEN`.
- **Inbound:** the web API requires its own key in the `X-API-Key` header and checks it against `MOVIE_API_KEY`.
- Secrets live only in environment variables. They are not stored in the repository.

## Roadmap

- [ ] AI-generated one-line movie pitch endpoint (planned)
- [ ] Retries with backoff on rate limits (HTTP 429) and timeouts
- [ ] Response caching

## What I practiced

REST APIs and HTTP methods, JSON parsing, API authentication, error handling, logging, unit testing with mocks, CI with GitHub Actions, and Git workflow.

## Attribution

This product uses the TMDB API but is not endorsed or certified by TMDB.
