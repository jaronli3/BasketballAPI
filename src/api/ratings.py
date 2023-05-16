from fastapi import APIRouter
import sqlalchemy
from src import database as db
from pydantic import BaseModel, conint

router = APIRouter()

class TeamRating(BaseModel):
    id: int
    rating: conint(ge=1, le=5)

@router.post("/teamratings/", tags=["ratings"])
def add_team_rating(team_rat: TeamRating):
    """
    This endpoint adds a user-generated team rating to the team_ratings table 
    * `team_rat`: contains the id (int) and rating (as int 1 --> 5) of the team 

    The endpoint returns the id of the newly generated team rating
    """

    # TODO get the team_id, from the team_name, within the one SQL query 

    with db.engine.connect() as conn:
        inserted_team_rating = conn.execute(
            sqlalchemy.text(
                '''
                INSERT INTO team_ratings (team_id, rating)
                VALUES (:team_id, :rating)
                RETURNING team_prediction_id;
            '''
            ),
            {
                "team_id": team_rat.id,
                "rating": team_rat.rating
            }
        )
        team_rating = inserted_team_rating.fetchone()
        conn.commit()
    return team_rating.team_prediction_id
