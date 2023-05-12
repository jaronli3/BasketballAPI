from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
import sqlalchemy
from fastapi.params import Query
from src import database as db
from typing import List, Dict
from pydantic import BaseModel

router = APIRouter()


@router.get("/athletes/{id}", tags=["athletes"])
def get_athlete(id: int,
                year: int = None
                ):
    """ 
    This endpoint returns a single athlete by its identifier. For each athlete it returns:
    * `athlete_id`: The internal id of the athlete
    * `name`: The name of the athlete

    If the year argument is specified, the endpoint returns athlete stats for that year.
    If the year argument is not specified, for each NBA season the athlete was a part of, the endpoint returns
    the year and stats of the athlete for that season.

    Athlete stats include:
    age, team_id, team_name, games_played, minutes_played, field_goal_percentage, free_throw_percentage,
    total_rebounds, assists, steals, blocks, points
    """

    athlete_name = sqlalchemy.select(db.athletes).where(db.athletes.c.athlete_id == id)
    athlete_stats = sqlalchemy.select(db.athlete_stats).where(db.athlete_stats.c.athlete_id == id)

    if year:  # Filter if year argument is passed
        athlete_stats = athlete_stats.where(db.athlete_stats.c.year == year)

    with db.engine.connect() as conn:
        athlete_name = conn.execute(athlete_name).fetchone()
        athlete_stats = conn.execute(athlete_stats).fetchall()
        if (not athlete_name) or (not athlete_stats):
            raise HTTPException(status_code=404, detail="athlete not found for the given year.")

        stats = [{
            "year": row.year,
            "age": row.age,
            "team_id": row.team_id,
            "team_name": conn.execute(sqlalchemy.select(db.teams.c.team_name)
                                      .where(db.teams.c.team_id == row.team_id)).fetchone().team_name,
            "games_played": row.games_played,
            "minutes_played": row.minutes_played,
            "field_goal_percentage": row.field_goal_percentage,
            "free_throw_percentage": row.free_throw_percentage,
            "total_rebounds": row.total_rebounds,
            "assists": row.assists,
            "steals": row.steals,
            "blocks": row.blocks,
            "points": row.points
        }
            for row in athlete_stats]

        json = {
            "athlete_id": id,
            "name": athlete_name.name,
            "stats": stats
        }

        return json


class StatOptions(str, Enum):
    games_played = "games_played"
    minutes_played = "minutes_played"
    field_goal_percentage = "field_goal_percentage"
    free_throw_percentage = "free_throw_percentage"
    total_rebounds = "total_rebounds"
    assists = "assists"
    steals = "steals"
    blocks = "blocks"
    points = "points"


@router.get("/athletes/", tags=["athletes"])
def compare_athletes(
        year: int,
        athlete_ids: List[int] = Query(None),
        stat: StatOptions = StatOptions.points,
):
    """ 
    This endpoint returns a comparison between the specified athletes, 
    and returns the athlete id, name, and stat as specified in the input.  
    It allows the user to compare athletes by a stat in `StatOptions`
    * `year`: the year to compare the athletes
    * `athlete_ids`: list of athlete names to compare (must have length >1)
    * `stat`: stat to compare athletes by (defaults to points)
    """

    if len(athlete_ids) < 2:
        raise HTTPException(status_code=400, detail="athlete list given does not contain enough athletes.")

    athlete_stats = (
        sqlalchemy.select(db.athlete_stats.c.athlete_id, sqlalchemy.column(stat).label('stat'))
            .where((sqlalchemy.column('athlete_id').in_(athlete_ids)) & (db.athlete_stats.c.year == year))
            .order_by(sqlalchemy.desc(sqlalchemy.column(stat)))
    )

    with db.engine.connect() as conn:
        result = conn.execute(athlete_stats)

        json = []
        for row in result.fetchall():
            json.append(
                {
                    "athlete_id": row.athlete_id,
                    "name": conn.execute(sqlalchemy.select(db.athletes.c.name)
                                      .where(db.athletes.c.athlete_id == row.athlete_id)).fetchone().name,
                    stat: row.stat
                }
            )

        return json


class AthleteJson(BaseModel):
    name: str
    age: int
    team: int
    stats: Dict[StatOptions, float] = {}


@router.post("/athletes/", tags=["athletes"])
def add_athlete(athlete: AthleteJson):
    """
    This endpoint adds an athlete to the database. The athlete is represented by the AthleteJson, which contains 
    * name: the name of the athlete
    * age: age of the athlete 
    * team: the team id of the athlete’s team
    * stats: a dictionary, matching StatOptions (such as "points") to values 
    The endpoint returns the id of the resulting athlete that was created
    """

    with db.engine.connect() as conn:
        team = conn.execute(
            sqlalchemy.text("""SELECT * FROM teams WHERE teams.team_id = :x"""),
            [{"x": athlete.team}]
        ).fetchone()
        if not team:
            raise HTTPException(status_code=404, detail="team not found.")

        new_athlete_id = conn.execute(
            sqlalchemy.text("""
            SELECT athletes.athlete_id
            FROM athletes
            ORDER BY athlete_id DESC
            LIMIT 1 
            """)
        ).fetchone().athlete_id + 1

        new_athlete = {
            "athlete_id": new_athlete_id,
            "name": athlete.name,
            "age": athlete.age,
            "team_id": athlete.team,
            "games_played": athlete.stats.get("games_played", None),
            "minutes_played": athlete.stats.get("minutes_played", None),
            "field_goal_percentage": athlete.stats.get("field_goal_percentage", None),
            "three_points_percentage": athlete.stats.get("three_points_percentage", None),
            "free_throw_percentage": athlete.stats.get("free_throw_percentage", None),
            "total_rebounds": athlete.stats.get("total_rebounds", None),
            "assists": athlete.stats.get("assists", None),
            "steals": athlete.stats.get("steals", None),
            "blocks": athlete.stats.get("blocks", None),
            "points": athlete.stats.get("points", None)
        }

        conn.execute(db.athletes.insert().values(**new_athlete))
        conn.commit()
        return new_athlete_id
