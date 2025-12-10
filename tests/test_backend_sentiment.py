# tests/test_backend_api.py
from fastapi.testclient import TestClient

from backend.sentiment_api import feelApp

client = TestClient(feelApp)

def test_sentiment():
    payload = {"texte": "It is a Wonderful Life !"}
    response = client.post("/analyse_sentiment/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["compound"] > 0