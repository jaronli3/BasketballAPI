from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
import sqlalchemy
from fastapi.params import Query
from src import database as db

router = APIRouter()


class team_options(str, Enum):
    toronto_raptors = "Toronto Raptors"
    memphis_grizzlies = "Memphis Grizzlies"
    miami_heat = "Miami Heat"
    utah_jazz = "Utah Jazz"
    milwaukee_bucks = "Milwaukee Bucks"
    cleveland_cavaliers = "Cleveland Cavaliers"
    new_orleans_pelicans = "New Orleans Pelicans"
    minnesota_timberwolves = "Minnesota Timberwolves"
    orlando_magic = "Orlando Magic"
    new_york_knicks = "New York Knicks"
    washington_wizards = "Washington Wizards"
    phoenix_suns = "Phoenix Suns"
    detriot_pistons = "Detroit Pistons"
    golden_state_warriors = "Golden State Warriors"
    charlotte_hornets = "Charlotte Hornets"
    san_antinio_spurs = "San Antonio Spurs"
    sacramento_kings = "Sacramento Kings"
    los_angeles_clippers = "Los Angeles Clippers"
    oklahoma_city_thunder = "Oklahoma City Thunder"
    dallas_mavericks = "Dallas Mavericks"
    los_angeles_lakers = "Los Angeles Lakers"
    indiana_pacers = "Indiana Pacers"
    atlanta_hawks = "Atlanta Hawks"
    chicago_bulls = "Chicago Bulls"
    denver_nuggets = "Denver Nuggets"
    boston_celtics = "Boston Celtics"
    portland_trail_blazers = "Portland Trail Blazers"
    philadelphia_76ers = "Philadelphia 76ers"
    houson_rockets = "Houston Rockets"
    brooklyn_nets = "Brooklyn Nets"


@router.get("/games/{id}", tags=["games"])
def get_game(
        home_team: team_options = team_options.toronto_raptors,
        away_team: team_options = team_options.milwaukee_bucks
):
    """
    This endpoint returns a single game by its identifier
        *game_id: internal id of game
        *home_team: name of home team
        *away_team: name of away team
        *winner_team: name of winner team
        *home_team_score: score of home team
        *away_team_score: score of away team
        *date: the date the game was held
    """
    if home_team == away_team:
        raise HTTPException(status_code=400, detail="Teams are the same")

    home_team_id = sqlalchemy.select(
        db.teams.c.team_id
    ).where(home_team == db.teams.c.team_name)

    away_team_id = sqlalchemy.select(
        db.teams.c.team_id
    ).where(away_team == db.teams.c.team_name)

    with db.engine.connect() as conn:
        home_team_id = conn.execute(home_team_id).fetchone().team_id
        away_team_id = conn.execute(away_team_id).fetchone().team_id

        result = conn.execute(
            sqlalchemy.select(
                db.games.c.game_id,
                db.games.c.home,
                db.games.c.away,
                db.games.c.winner,
                db.games.c.pts_home,
                db.games.c.pts_away,
                db.games.c.date
            ).where((db.games.c.home == home_team_id) & (db.games.c.away == away_team_id))
        ).fetchall()

        json = [
            {"game_id": game.game_id,
             "home_team": home_team.value,
             "away_team": away_team.value,
             "winner": home_team.value if game.winner == game.home else away_team.value,
             "home_team_score": game.pts_home,
             "away_team_score": game.pts_away,
             "date": str(game.date)}
            for game in result
        ]
        return json
