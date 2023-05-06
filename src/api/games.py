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


@router.get("/games/", tags=["games"])
def get_game(
        home_team: team_options = team_options.toronto_raptors,
        away_team: team_options = team_options.milwaukee_bucks
):
    """
    This endpoint returns a list of games by the teams provided ordered by date

    For each game it returns:
        *`game_id`: internal id of game
        *`home_team`: name of home team
        *`away_team`: name of away team
        *`winner_team`: name of winner team
        *`home_team_score`: score of home team
        *`away_team_score`: score of away team
        *`date`: the date the game was held
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
                .order_by(db.games.c.date)
        ).fetchall()

        if len(result) == 0:
            raise HTTPException(status_code=404, detail="No games found")

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


def add_game(
        home_team: team_options,
        away_team: team_options,
        winner: team_options,
        date: str = None,
        points_home: int = None,
        points_away: int = None,
        three_pointer_percent_home: float = None,
        three_pointer_percent_away: float = None,
        rebounds_home: int = None,
        rebounds_away: int = None,
        assists_home: int = None,
        assists_away: int = None,
        steals_home: int = None,
        steals_away: int = None,
        blocks_home: int = None,
        blocks_away: int = None
):
    """
    This endpoint adds a game to the database. The game is represented by:
        *`home_team_id`: the id of the home team
        *`away_team_id`: the id of the away team
        *`winner_id`: the id of the winner’s team
        *Additional statistics about the game

    The endpoint returns the id of the game created
    """
    if home_team == away_team:
        raise HTTPException(status_code=400, detail="Teams are the same")
    if winner != home_team and winner != away_team:
        raise HTTPException(status_code=400, detail="Select a valid winner")

    with db.engine.connect() as conn:
        game_id = conn.execute(
            sqlalchemy.select(
                db.games.c.game_id
            )
            .order_by(sqlalchemy.desc(db.games.c.game_id))
            .limit(1)
        ).fetchone().game_id + 1

        home_team_id = conn.execute(
            sqlalchemy.select(
                db.teams.c.team_id
            ).where(db.teams.c.team_name == home_team)
        ).fetchone().team_id

        away_team_id = conn.execute(
            sqlalchemy.select(
                db.teams.c.team_id
            ).where(db.teams.c.team_name == away_team)
        ).fetchone().team_id

        game = {
            "game_id": game_id,
            "home": home_team_id,
            "away": away_team_id,
            "winner": home_team_id if home_team == winner else away_team_id,
            "date": date,

        }

add_game(team_options.milwaukee_bucks, team_options.toronto_raptors, team_options.milwaukee_bucks)
