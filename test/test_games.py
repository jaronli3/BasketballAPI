from fastapi.testclient import TestClient

from src.api.server import app
from src.api.games import add_game, team_options
from src import database as db
import datetime

import json

client = TestClient(app)


def test_get_games():
    response = client.get("/games/?home_team=Toronto%20Raptors&away_team=Milwaukee%20Bucks")
    assert response.status_code == 200

    with open("test/games/raptors_bucks.json") as f:
        assert response.json() == json.load(f)


def test_get_games_2():
    response = client.get("/games/?home_team=Golden%20State%20Warriors&away_team=Los%20Angeles%20Clippers")
    assert response.status_code == 200

    with open("test/games/warriors_clippers.json") as f:
        assert response.json() == json.load(f)


def test_get_game_same_team():
    response = client.get("/games/?home_team=Brooklyn%20Nets&away_team=Brooklyn%20Nets")
    assert response.status_code == 400


def test_add_game():
    game_id = add_game(
        team_options.brooklyn_nets,
        team_options.houson_rockets,
        datetime.date(2023, 3, 30),
        100, 99, 30.1, 28.4, 5, 4, 9, 2, 4, 3, 2, 1
    )
    response = client.get("/games/?home_team=Brooklyn%20Nets&away_team=Houston%20Rockets")
    assert response.status_code == 200

    with open("test/games/nets_rockets_test_add.json") as f:
        assert response.json() == json.load(f)

    with db.engine.connect() as conn:
        conn.execute(
            db.games.delete().where(db.games.c.game_id == game_id)
        )

        conn.commit()


def test_add_game_same_team():
    response = client.get("/games/add_game?home_team=Toronto%20Raptors&away_team=Toronto%20Raptors")
    assert response.status_code == 400
