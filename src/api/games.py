from fastapi import APIRouter, HTTPException
import sqlalchemy
from datetime import date
from src import database as db
from src.api.teams import team_options
from pydantic import BaseModel


router = APIRouter()


@router.get("/games/", tags=["games"])
def get_game(
        home_team: team_options,
        away_team: team_options,
        winner: team_options = None
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
    if home_team == away_team:
        raise HTTPException(status_code=400, detail="Teams are the same")

    if winner and not(winner == home_team or winner == away_team):
        raise HTTPException(status_code=400, detail="Please select a valid winner")

    home_team_id_stmt = sqlalchemy.select(
        db.teams.c.team_id
    ).where(home_team == db.teams.c.team_name)

    away_team_id_stmt = sqlalchemy.select(
        db.teams.c.team_id
    ).where(away_team == db.teams.c.team_name)

    with db.engine.begin() as conn:
        home_team_id = conn.execute(home_team_id_stmt).scalar_one()
        away_team_id = conn.execute(away_team_id_stmt).scalar_one()

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

        json = [
            {"game_id": game.game_id,
             "home_team": home_team.value,
             "away_team": away_team.value,
             "winner": home_team.value if game.pts_home > game.pts_away else away_team.value,
             "home_team_score": game.pts_home,
             "away_team_score": game.pts_away,
             "date": str(game.date)}
            for game in result
        ]

        if winner:
            json = [game for game in json if game.get("winner") == winner.value]

        return json


class GameJson(BaseModel):
    home_team: team_options
    away_team: team_options
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
    if game.home_team == game.away_team:
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

        home_team_id = conn.execute(
            sqlalchemy.select(
                db.teams.c.team_id
            ).where(db.teams.c.team_name == game.home_team)
        ).scalar_one()

        away_team_id = conn.execute(
            sqlalchemy.select(
                db.teams.c.team_id
            ).where(db.teams.c.team_name == game.away_team)
        ).scalar_one()

        game = {
            "game_id": game_id,
            "home": home_team_id,
            "away": away_team_id,
            "winner": home_team_id if game.points_home > game.points_away else away_team_id,
            "date": date,
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
        conn.execute(db.games.insert().values(**game))

    return game_id
