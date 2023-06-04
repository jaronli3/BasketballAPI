from fastapi import APIRouter, HTTPException
import sqlalchemy
from src import database as db
from pydantic import BaseModel, conint

router = APIRouter()


class Rating(BaseModel):
    id: int
    rating: conint(ge=1, le=5)


@router.post("/teamratings/", tags=["ratings"])
def add_team_rating(rat: Rating):
    """
    This endpoint adds a user-generated team rating to the team_ratings table 
    * `rating`: contains the team id (int) and rating (as a number 1 through 5) of the team

    The endpoint returns the name of the rated team
    """

    team_name_stmt = sqlalchemy.select(db.teams.c.team_name).where(db.teams.c.team_id == rat.id)

    with db.engine.begin() as conn:

        team_name = conn.execute(team_name_stmt).fetchone()

        if not team_name:
            raise HTTPException(status_code=404, detail="team not found.")

        conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO team_ratings (team_id, rating)
                VALUES (:team_id, :rating)
            """
            ),
            {
                "team_id": rat.id,
                "rating": rat.rating
            }
        )

    return team_name.team_name


@router.post("/athleteratings/", tags=["ratings"])
def add_athlete_rating(rat: Rating):
    """
    This endpoint adds a user-generated athlete rating to the athlete_ratings table
    * `rating`: contains the athlete id (int) and rating (as a number 1 through 5) of the athlete

    The endpoint returns the name of the rated athlete
    """

    athlete_name_stmt = sqlalchemy.select(db.athletes.c.name).where(db.athletes.c.athlete_id == rat.id)

    with db.engine.begin() as conn:
        athlete_name = conn.execute(athlete_name_stmt).fetchone()

        if not athlete_name:
            raise HTTPException(status_code=404, detail="athlete not found.")

        conn.execute(
            sqlalchemy.text(
                """
                INSERT INTO athlete_ratings (athlete_id, rating)
                VALUES (:athlete_id, :rating)
            """
            ),
            {
                "athlete_id": rat.id,
                "rating": rat.rating
            }
        )

    return athlete_name.name
