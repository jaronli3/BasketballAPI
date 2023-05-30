from fastapi import APIRouter, HTTPException
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
    * `rat`: contains the team name (str) and rating (as a number 1 --> 5) of the team 

    The endpoint returns the id of the newly generated team rating
    """

    with db.engine.begin() as conn:
        try:
            team_id = conn.execute(
                sqlalchemy.text(
                    """
                    SELECT team_id
                    FROM teams
                    WHERE team_name = :team_name
                """
                ),
                {
                    "team_name": rat.name,
                }
            ).scalar_one()
        except:
            raise HTTPException(status_code=404, detail="team not found.")

        inserted_rating = conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO team_ratings (team_id, rating)
                VALUES (:team_id, :rating)
                RETURNING team_rating_id
            """
            ),
            {
                "team_id": team_id,
                "rating": rat.rating
            }
        ).scalar_one()

    return inserted_rating


@router.post("/athleteratings/", tags=["ratings"])
def add_athlete_rating(rat: Rating):
    """
    This endpoint adds a user-generated athlete rating to the athlete_ratings table 
    * `rat`: contains the athlete name (str) and rating (as a number 1 --> 5) of the team 

    The endpoint returns the id of the newly generated athlete rating
    """

    with db.engine.begin() as conn:
        try:
            athlete_id = conn.execute(
                sqlalchemy.text(
                    """
                    SELECT athlete_id
                    FROM athletes
                    WHERE name = :athlete_name
                """
                ),
                {
                    "athlete_name": rat.name,
                }
            ).scalar_one()
        except:
            raise HTTPException(status_code=404, detail="athlete not found.")

        inserted_rating = conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO athlete_ratings (athlete_id, rating)
                VALUES (:athlete_id, :rating)
                RETURNING athlete_rating_id
            """
            ),
            {
                "athlete_id": athlete_id,
                "rating": rat.rating
            }
        ).scalar_one()

    return inserted_rating
