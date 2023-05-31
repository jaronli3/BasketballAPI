from fastapi import APIRouter, HTTPException
import sqlalchemy
from datetime import date
from src import database as db
from pydantic import BaseModel
from enum import Enum

router = APIRouter()


class winner_options(str, Enum):
    home = "home"
    away = "away"


@router.get("/games/", tags=["games"])
def get_game(
        home_team_id: int,
        away_team_id: int,
        winner: winner_options = None
):
    """
    This endpoint returns a list of games by the teams provided ordered by date

    For each game it returns:
    * `game_id`: internal id of game
    * `home_team`: name of home team
    * `away_team`: name of away team
    * `winner_team`: name of winner team
    * `home_team_score`: score of home team
    * `away_team_score`: score of away team
    * `date`: the date the game was held
    """
    if home_team_id == away_team_id:
        raise HTTPException(status_code=400, detail="Home team and away team cannot be the same")

    home_team_stmt = sqlalchemy.select(db.teams.c.team_name).where(db.teams.c.team_id == home_team_id)
    away_team_stmt = sqlalchemy.select(db.teams.c.team_name).where(db.teams.c.team_id == away_team_id)

    with db.engine.begin() as conn:
        result = conn.execute(
            sqlalchemy.select(
                db.games.c.game_id,
                db.games.c.home,
                db.games.c.away,
                db.games.c.pts_home,
                db.games.c.pts_away,
                db.games.c.date
            ).where((db.games.c.home == home_team_id) & (db.games.c.away == away_team_id))
                .order_by(db.games.c.date)
        ).fetchall()

        if len(result) == 0:
            raise HTTPException(status_code=404, detail="No games found")

        home_team = conn.execute(home_team_stmt).scalar_one()
        away_team = conn.execute(away_team_stmt).scalar_one()

        json = [
            {"game_id": game.game_id,
             "home_team": home_team,
             "away_team": away_team,
             "winner": home_team if game.pts_home > game.pts_away else away_team,
             "home_team_score": game.pts_home,
             "away_team_score": game.pts_away,
             "date": str(game.date)}
            for game in result
        ]

        if winner == winner_options.home:
            json = [game for game in json if game.get("winner") == home_team]
        elif winner == winner_options.away:
            json = [game for game in json if game.get("winner") == away_team]

        return json


class GameJson(BaseModel):
    home_team_id: int
    away_team_id: int
    date: date
    points_home: int
    points_away: int
    rebounds_home: int
    rebounds_away: int
    assists_home: int
    assists_away: int
    steals_home: int
    steals_away: int
    blocks_home: int
    blocks_away: int


@router.post("/games/add_game", tags=["games"])
def add_game(game: GameJson):
    """
    This endpoint adds a game to the database. The game is represented by:
    * `home_team_id`: the id of the home team
    * `away_team_id`: the id of the away team
    * `winner_id`: the id of the winner’s team
    * Additional statistics about the game

    The endpoint returns the id of the game created
    """
    if game.home_team_id == game.away_team_id:
        raise HTTPException(status_code=400, detail="Teams are the same")

    if game.points_home == game.points_away:
        raise HTTPException(status_code=400, detail="Point values cannot be equal")

    with db.engine.begin() as conn:
        game_id = conn.execute(
            sqlalchemy.select(
                db.games.c.game_id
            )
            .order_by(sqlalchemy.desc(db.games.c.game_id))
            .limit(1)
        ).scalar_one() + 1

        postgame = {
            "game_id": game_id,
            "home": game.home_team_id,
            "away": game.away_team_id,
            "date": game.date,
            "pts_home": game.points_home,
            "pts_away": game.points_away,
            "reb_home": game.rebounds_home,
            "reb_away": game.rebounds_away,
            "ast_home": game.assists_home,
            "ast_away": game.assists_away,
            "stl_home": game.steals_home,
            "stl_away": game.steals_away,
            "blk_home": game.blocks_home,
            "blk_away": game.blocks_away
        }
        conn.execute(db.games.insert().values(**postgame))

    return game_id
