from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_athlete():
    response = client.get("/athletes/321")
    assert response.status_code == 200
    
    with open("test/athletes/321.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_athlete_404():
    response = client.get("/athletes/10001")
    assert response.status_code == 404

def test_compare_athletes_1():
    params = {
        "athlete_names": ["LeBron James", "Stephen Curry", "Cole Anthony"],
        "stat": "points"
    }

    response = client.get("/athletes/", params=params)

    with open("test/athletes/compare_athletes_1.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_compare_athletes_2():
    params = {
        "athlete_names": ["LeBron James", "Stephen Curry", "Cole Anthony"],
        "stat": "games_played"
    }

    response = client.get("/athletes/", params=params)

    with open("test/athletes/compare_athletes_2.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_compare_athletes_400():
    params = {
        "athlete_names": ["LeBron James"],
        "stat": "points"
    }

    response = client.get("/athletes/", params=params)
    assert response.status_code == 400

def test_add_athlete():
    athlete_data = {
        "name": "Bob Ben",
        "age": 199,
        "team": 4,
        "stats": {
            "games_played": 1,
            "points": 200,
            "blocks": 2
        }
    }
    response = client.post("/athletes/", json=athlete_data)
    assert response.status_code == 200

    athlete_response = client.get("/athletes/" + response.content.decode('utf-8'))
    assert athlete_response.status_code == 200

def test_add_athlete_2():
    athlete_data = {
        "name": "New Athlete Name",
        "age": 55,
        "team": 10,
        "stats": {
        }
    }
    response = client.post("/athletes/", json=athlete_data)
    assert response.status_code == 200

    athlete_response = client.get("/athletes/" + response.content.decode('utf-8'))
    assert athlete_response.status_code == 200

def test_add_athlete_404():
    athlete_data = {
        "name": "New Athlete Name",
        "age": 55,
        "team": 200,
        "stats": {
        }
    }
    response = client.post("/athletes/", json=athlete_data)
    assert response.status_code == 404
