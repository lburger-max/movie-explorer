from unittest.mock import patch, MagicMock
import movie_explorer


@patch("movie_explorer.requests.get")
def test_search_movies_returns_results(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"results": [{"title": "Inception", "id": 27205}]}
    mock_get.return_value = mock_response

    results = movie_explorer.search_movies("inception")

    assert results[0]["title"] == "Inception"
