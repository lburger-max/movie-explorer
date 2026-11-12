git clone <your-repo-url> && cd movie-explorer
python3 -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install requests pytest
export TMDB_READ_ACCESS_TOKEN="eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxOWEyOGFhYzRiODBjNzg5MDhjNjkwOTVjZGU5OTViNCIsIm5iZiI6MTc5NDQ2MjY1MS4yMzMsInN1YiI6IjZhZjU1M2JiZWQyNjUzMDFlYWQ2N2E5NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.MavaJR07xbVkDzCyjYNy0aVzlD-mm5hcwOozSptXqNs"   # Windows: set TMDB_READ_ACCESS_TOKEN=...
echo "venv/" >> .gitignore && echo ".env" >> .gitignore
