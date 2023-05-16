from fastapi import APIRouter
import sqlalchemy
from src import database as db
from pydantic import BaseModel, conint

router = APIRouter()

class TeamRating(BaseModel):
    name: str
    rating: conint(ge=1, le=5)

@router.post("/teamratings/", tags=["ratings"])
def add_team_rating(team_rat: TeamRating):
    """
    This endpoint adds a user-generated team rating to the team_ratings table 
    * `team_rat`: contains the team name (str) and rating (as int 1 --> 5) of the team 

    The endpoint returns the id of the newly generated team rating
    """

    with db.engine.connect() as conn:
        inserted_team_rating = conn.execute(
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
                "team_name": team_rat.name,
                "rating": team_rat.rating
            }
        )
        team_rating = inserted_team_rating.fetchone()
        conn.commit()
    return team_rating.team_prediction_id
