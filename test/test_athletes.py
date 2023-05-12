from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)
prefix="/Users/zach/Desktop/CSC_365/Project/"

def test_get_athlete():
    response = client.get("/athletes/321")
    assert response.status_code == 200
    
    with open("test/athletes/321.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_get_athlete_404():
    response = client.get("/athletes/10001")
    assert response.status_code == 404


def test_compare_athletes_1():
    response = client.get("/athletes/?year=2023&athlete_ids=0&athlete_ids=1&athlete_ids=2&athlete_ids=3&athlete_ids=4&stat=points")
    assert response.status_code == 200

    with open("test/athletes/compare_athletes_1.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_compare_athletes_2():
    response = client.get("/athletes/?year=2023&athlete_ids=200&athlete_ids=184&athlete_ids=233&athlete_ids=154&athlete_ids=192&stat=games_played")

    with open("test/athletes/compare_athletes_2.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_compare_athletes_400():
    response = client.get("/athletes/?year=2023&athlete_ids=0&stat=games_played")
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
