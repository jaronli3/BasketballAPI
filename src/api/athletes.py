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
def get_athlete(id: int, year = None):
    """ 
    This endpoint returns a single athlete by its identifier. For each athlete it returns:
    * `athlete_id`: The internal id of the athlete.
    * `name`: The name of the athlete
    * `team_id`: The team id the athlete plays for
    * `age`: The age of the athlete
    * `stats`: a json returning some of the stats of the athlete
    * games_played, minutes_played, field_goal_percentage, three_point_percentage, free_throw_percentage, total_rebounds, assist, steals, blocks, points 
    """
    if year is None:
        stmt = (sqlalchemy.select(db.athletes).where(db.athletes.c.athlete_id == id))
        stmt1 = sqlalchemy.select(db.athlete_stats).where(db.athlete_stats.c.athlete_id == id)

        with db.engine.connect() as conn:
            res = conn.execute(stmt).fetchone()
            res1 = conn.execute(stmt1).fetchall()
            if res is None or rest1 is None:
                raise HTTPException(status_code=404, detail="athlete not found.")

            games_played = 0
            minutes_played = 0
            field_goal_percentage = 0
            free_throw_percentage = 0
            three_points_percentage = 0
            total_rebounds = 0
            assists = 0
            steals = 0
            blocks = 0
            points = 0

            for row in res1:
                games_played += row.games_played
                minutes_played += row.minutes_played
                field_goal_percentage += row.field_goal_percentage
                three_points_percentage += row.three_point_percentage
                free_throw_percentage += row.free_throw_percentage
                total_rebounds += row.total_rebounds
                assists += row.assists
                steals += row.steals
                blocks += row.blocks
                points += row.points

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
    
class StatOptions(str, Enum):
    games_played = "games_played"
    minutes_played = "minutes_played"
    field_goal_percentage = "field_goal_percentage"
    three_points_percentage = "three_points_percentage"
    free_throw_percentage = "free_throw_percentage"
    total_rebounds = "total_rebounds"
    assists = "assists"
    steals = "steals"
    blocks = "blocks"
    points = "points"
    
@router.get("/athletes/", tags=["athletes"])
def compare_athletes(
    athlete_names: List[str] = Query(None),
    stat: StatOptions = StatOptions.points
    ):
    """ 
    This endpoint returns a comparison between the specified athletes, 
    and returns the athlete id, name, and stat as specified in the input.  
    It allows the user to compare athletes by a stat in `StatOptions` 
    * `athlete_names`: list of athlete names to compare (must have length >1)
    * `stat`: stat to compare athletes by (defaults to points)
    """
    
    if len(athlete_names) < 2:
        raise HTTPException(status_code=400, detail="athlete list given does not contain enough althletes.")

    stmt = (
        sqlalchemy.select(db.athletes.c.athlete_id, db.athletes.c.name, sqlalchemy.column(stat).label('stat'))
        .where(sqlalchemy.column('name').in_(athlete_names))
        .order_by(sqlalchemy.column(stat))
    )

    with db.engine.connect() as conn:
        result = conn.execute(stmt)

        json = []
        for row in result.fetchall():
            json.append(
                {
                    "athlete_id": row.athlete_id,
                    "name": row.name,
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
