from fastapi.testclient import TestClient
from fastapi import HTTPException

from src.api.server import app
from src.api.ratings import *
from src import database as db

client = TestClient(app)

def test_add_team_rating():
    reqbody = {
        "name": "Utah Jazz",
        "rating": 2
    }
    response = client.post("/teamratings/", json=reqbody)
    assert response.status_code == 200

def test_add_team_rating_404():
    reqbody = {
        "name": "not a teams name",
        "rating": 3
    }
    response = client.post("/teamratings/", json=reqbody)
    assert response.status_code == 404

def test_add_athlete_rating():
    reqbody = {
        "name": "Stephen Curry",
        "rating": 2
    }
    response = client.post("/athleteratings/", json=reqbody)
    assert response.status_code == 200

def test_add_athlete_rating_404():
    reqbody = {
        "name": "not a players name",
        "rating": 3
    }
    response = client.post("/athleteratings/", json=reqbody)
    assert response.status_code == 404
