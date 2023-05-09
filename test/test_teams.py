from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_teams1():
    response = client.get("/teams/14")
    assert response.status_code == 200
    
    with open("test/teams/14.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)
    

def test_get_teams2():
    response = client.get("/teams/27")
    assert response.status_code == 200
    
    with open("test/teams/27.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)
    

def test_compare_teams1():
    params = {
        "teams": ["Portland Trail Blazers", "Golden State Warriors"],
        "compare_by": "average three point percentage"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/blazers_warriors.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_compare_teams2():
    params = {
        "teams": ["Cleveland Cavaliers", "Boston Celtics"],
        "compare_by": "blocks"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/cavaliers_celtics.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_compare_teams3():
    params = {
        "teams": ["Cleveland Cavaliers", "Utah Jazz"],
        "compare_by": "steals"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/cavaliers_jazz.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_compare_teams4():
    params = {
        "teams": ["Los Angeles Clippers", "Golden State Warriors", "Boston Celtics"],
        "compare_by": "wins"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/clippers_warriors_celtics.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_compare_teams5():
    params = {
        "teams": ["Los Angeles Lakers", "Golden State Warriors"],
        "compare_by": "rebounds"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/lakers_warriors.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_compare_teams6():
    params = {
        "teams": ["Dallas Mavericks", "Brooklyn Nets"],
        "compare_by": "assists"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/mavericks_nets.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)
    
def test_compare_teams7():
    params = {
        "teams": ["New Orleans Pelicans", "Charlotte Hornets", "Boston Celtics", "Houston Rockets"],
        "compare_by": "points"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/pelicans_hornets_celtics_rockets.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_404():
    response = client.get("/teams/30")
    assert response.status_code == 404
