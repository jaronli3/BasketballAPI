from fastapi import APIRouter
import sqlalchemy
from src import database as db
from pydantic import BaseModel, conint

router = APIRouter()

class Rating(BaseModel):
    name: str
    rating: conint(ge=1, le=5)

@router.post("/teamratings/", tags=["ratings"])
def add_team_rating(rat: Rating):
    """
    This endpoint adds a user-generated team rating to the team_ratings table 
    * `rat`: contains the team name (str) and rating (as int 1 --> 5) of the team 

    The endpoint returns the id of the newly generated team rating
    """

    with db.engine.connect() as conn:
        inserted_rating = conn.execute(
            sqlalchemy.text(
            """
                INSERT INTO team_ratings (team_id, rating)
                SELECT team_id
                FROM teams
                WHERE team_name = :team_name
                RETURNING team_prediction_id
            """
            ),
            {
                "team_name": rat.name,
                "rating": rat.rating
            }
        )
        rating = inserted_rating.fetchone()
        conn.commit()
    return rating.team_prediction_id

@router.post("/athleteratings/", tags=["ratings"])
def add_athlete_rating(rat: Rating):
    """
    This endpoint adds a user-generated athlete rating to the athlete_ratings table 
    * `rat`: contains the athlete name (str) and rating (as int 1 --> 5) of the team 

    The endpoint returns the id of the newly generated athlete rating
    """

    with db.engine.connect() as conn:
        inserted_rating = conn.execute(
            sqlalchemy.text(
            """
                INSERT INTO athlete_ratings (athlete_id, rating)
                SELECT athlete_id
                FROM athletes
                WHERE name = :athlete_name
                RETURNING athlete_rating_id
            """
            ),
            {
                "athlete_name": rat.name,
                "rating": rat.rating
            }
        )
        rating = inserted_rating.fetchone()
        conn.commit()
    return rating.athlete_rating_id

