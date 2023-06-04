from fastapi import APIRouter, HTTPException
import sqlalchemy
from src import database as db
from src.api import athletes, teams
from src.api.prediction_utils import * 

router = APIRouter()

@router.get("/predictions/team", tags=["predictions"])
def get_team_market_price(team_id: int):
    """
    This endpoint returns the current market price of the specified team
    """

    # read team stats and team ratings 
    team_stats_json = teams.get_team(team_id).get("team_stats")

    ratings_stmt = sqlalchemy.select(db.team_ratings.c.rating).where(db.team_ratings.c.team_id == team_id)

    if ratings_stmt is None:
        raise HTTPException(status_code=404, detail="team not found")

    with db.engine.begin() as conn:
        ratings = conn.execute(ratings_stmt).fetchall()

    ratings = [rating_instance.rating for rating_instance in ratings]

    # do calculations 
    return calc_team_market_price(team_stats_json, ratings)
   
@router.get("/predictions/athlete", tags=["predictions"])
def get_athlete_market_price(id: int):
    """
    This endpoint returns the current market price of the specified athlete
    * `id` the id of the athlete 
    """

    # read athlete stats and ratings 
    athlete_stats_json = athletes.get_athlete(id).get("stats")

    if len(athlete_stats_json) == 0:
        raise HTTPException(status_code=400, detail="athlete has no data associated with them")

    if len(athlete_stats_json) == 1:
        raise HTTPException(status_code=400, detail="athlete needs at least two seasons of data for a valid prediction")

    stmt = sqlalchemy.select(db.max_athlete_stats)
    ratings_stmt = sqlalchemy.select(db.athlete_ratings.c.rating).where(db.athlete_ratings.c.athlete_id == id)

    with db.engine.begin() as conn:
        result = conn.execute(stmt).fetchone()
        ratings = conn.execute(ratings_stmt).fetchall()

    # do calculations 
    return calc_athlete_market_price(athlete_stats_json, ratings, result)
