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
    * `sport`: The sport the athlete plays
    * `team`: The team the athlete plays for
    * `gender`: The gender of the athlete
    * `age`: The age of the athlete
    * `years`: the years they played
    * `stats`: a json returning some of the stats of the athlete
    * `stats` is represented by a dictionary in which the keys are dependent on the sport 
    the athlete plays. For example, if the athlete plays baseball, stats will include batting average.
    """

    return {"gg": 1}

    # with db.engine.connect() as conn:
    #     result_a = conn.execute(
    #         sqlalchemy.text("""
    #         SELECT
    #             characters.character_id,
    #             characters.name AS character,
    #             movies.title AS movie,
    #             characters.gender
    #         FROM characters
    #         JOIN movies ON characters.movie_id = movies.movie_id
    #         WHERE characters.character_id = :x
    #         """), [{"x": id}]
    #     ).fetchone()

