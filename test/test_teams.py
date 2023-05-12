from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_teams1():
    response = client.get("/teams/Charlotte%20Hornets/2023")
    assert response.status_code == 200
    
    with open("test/teams/hornets_2023.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)
    

def test_get_teams2():
    response = client.get("/teams/Philadelphia%2076ers/2019")
    assert response.status_code == 200
    
    with open("test/teams/phili_2019.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_compare_teams1():
    params = {
        "team_1": "Cleveland Cavaliers",
        "team_2": "Boston Celtics",
        "compare_by": "blocks"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/cavaliers_celtics.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_compare_teams2():
    params = {
        "team_1": "Cleveland Cavaliers",
        "team_2": "Utah Jazz",
        "compare_by": "steals"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/cavaliers_jazz.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_compare_teams3():
    params = {
        "team_1": "Los Angeles Clippers",
        "team_2": "Golden State Warriors",
        "team_3": "Boston Celtics",
        "compare_by": "wins"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/clippers_warriors_celtics.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_compare_teams4():
    params = {
        "team_1": "Los Angeles Lakers",
        "team_2": "Golden State Warriors",
        "compare_by": "rebounds"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/lakers_warriors.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_compare_teams5():
    params = {
        "team_1": "Dallas Mavericks",
        "team_2": "Brooklyn Nets",
        "compare_by": "assists"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/mavericks_nets.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_compare_teams6():
    params = {
        "team_1": "New Orleans Pelicans",
        "team_2": "Charlotte Hornets",
        "team_3": "Boston Celtics",
        "team_4": "Houston Rockets",
        "compare_by": "points"
    }

    response = client.get("/teams/", params=params)

    with open("test/teams/pelicans_hornets_celtics_rockets.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)
