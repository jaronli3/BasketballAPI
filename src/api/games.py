from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
import sqlalchemy
from fastapi.params import Query
from src import database as db

router = APIRouter()


@router.get("/games/{id}", tags=["games"])
def get_game(id: int):
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
    stmt = sqlalchemy.select(
        db.games.c.game_id,
        db.games.c.home,
        db.games.c.away,
        db.games.c.winner,
        db.games.c.pts_home,
        db.games.c.pts_away,
        db.games.c.date
    ).where(db.games.c.game_id == id)

    with db.engine.connect() as conn:
        result = conn.execute(stmt).fetchone()

        home_team = conn.execute(
            sqlalchemy.select(
                db.teams.c.team_name
            ).where(db.teams.c.team_id == result.home)
        ).fetchone()

        away_team = conn.execute(
            sqlalchemy.select(
                db.teams.c.team_name
            ).where(db.teams.c.team_id == result.away)
        ).fetchone()

        json = {"game_id": result.game_id,
                "home_team": home_team.team_name,
                "away_team": away_team.team_name,
                "winner": home_team.team_name if result.winner == result.home else away_team.team_name,
                "home_team_score": result.pts_home,
                "away_team_score": result.pts_away,
                "date": str(result.date)
        }
        return json
