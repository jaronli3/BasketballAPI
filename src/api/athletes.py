from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
import sqlalchemy
from fastapi.params import Query
from src import database as db

router = APIRouter()

@router.get("/athletes/{id}", tags=["athletes"])
def get_athlete(id: int):
    """ 
    This endpoint returns a single athlete by its identifier. For each athlete it returns:
    * `athlete_id`: The internal id of the athlete.
    * `name`: The name of the athlete
    * `team_id`: The team id the athlete plays for
    * `age`: The age of the athlete
    * `stats`: a json returning some of the stats of the athlete
    * games_played, minutes_played, field_goal_percentage, three_point_percentage, free_throw_percentage, total_rebounds, assist, steals, blocks, points 
    """

    stmt = (sqlalchemy.select(db.athletes).where(db.athletes.c.athlete_id == id))

    with db.engine.connect() as conn:
        res = conn.execute(stmt).fetchone()
        if res is None:
            raise HTTPException(status_code=404, detail="athlete not found.")

        stats = {
            "games_played": res.games_played,
            "minutes_played": res.minutes_played,
            "field_goal_percentage": res.field_goal_percentage,
            "three_points_percentage": res.three_points_percentage,
            "free_throw_percentage": res.free_throw_percentage,
            "total_rebounds": res.total_rebounds,
            "assists": res.assists,
            "steals": res.steals,
            "blocks": res.blocks,
            "points": res.points
        }

        return {
            "athlete_id": res.athlete_id,
            "name": res.name,
            "team_id": res.team_id,
            "age": res.age,
            "stats": stats
        }
