from fastapi.testclient import TestClient
from fastapi import APIRouter, HTTPException

from src.api.server import app
from src.api.athletes import AthleteStats, AthleteJson, add_athlete, add_athlete_season
from src import database as db

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
    with db.engine.begin() as conn:
        athlete_id = add_athlete("Test Athlete")
        stats = AthleteStats(games_played=0, minutes_played=0, field_goal_percentage=0.0,
                             free_throw_percentage=0.0, total_rebounds=0, assists=0, steals=0, blocks=0, turnovers=0, points=0)
        athlete_json = AthleteJson(athlete_id=athlete_id, age=0, year=2023, team_id=0, stats=stats)
        add_athlete_season(athlete_json)

        response = client.get("/athletes/" + str(athlete_id))
        assert response.status_code == 200

        with open("test/athletes/test_add_athlete.json", encoding="utf-8") as f:
            assert response.json() == json.load(f)

        conn.execute(
            db.athletes.delete().where(db.athletes.c.athlete_id == athlete_id)
        )
        conn.execute(
            db.athlete_stats.delete().where(db.athlete_stats.c.athlete_id == athlete_id)
        )


def test_add_athlete_400():
    try:
        add_athlete(name="Stephen Curry")
        assert False
    except HTTPException:
        pass


def test_add_season_errors():
    stats = AthleteStats(games_played=0, minutes_played=0, field_goal_percentage=0.0,
                         free_throw_percentage=0.0, total_rebounds=0, assists=0, steals=0, blocks=0, turnovers=0,
                         points=0)
    # Invalid athlete_id
    athlete_json = AthleteJson(athlete_id=100001, age=0, year=2023, team_id=0, stats=stats)
    try:
        add_athlete_season(athlete_json)
        assert False
    except HTTPException:
        pass

    # Invalid team_id
    athlete_json = AthleteJson(athlete_id=0, age=0, year=2023, team_id=100, stats=stats)
    try:
        add_athlete_season(athlete_json)
        assert False
    except HTTPException:
        pass

    # Athlete year pair already exists
    athlete_json = AthleteJson(athlete_id=0, age=0, year=2023, team_id=0, stats=stats)
    try:
        add_athlete_season(athlete_json)
        assert False
    except HTTPException:
        pass

