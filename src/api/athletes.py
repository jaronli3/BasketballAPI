from fastapi import APIRouter, HTTPException
from enum import Enum
import sqlalchemy
from fastapi.params import Query
from sqlalchemy.exc import IntegrityError

from src import database as db
from typing import List
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
    * `TEMP`

    If the year argument is specified, the endpoint returns athlete stats for that year.
    If the year argument is not specified, for each NBA season the athlete was a part of, the endpoint returns
    the year and stats of the athlete for that season.

    Athlete stats include:
    age, team_id, team_name, games_played, minutes_played, field_goal_percentage, free_throw_percentage,
    total_rebounds, assists, steals, blocks, points
    """
    if year and not (2019 <= year <= 2023):
        raise HTTPException(status_code=400, detail="please enter a year within 2019 to 2023 (inclusive)")

    athlete = sqlalchemy.select(db.athlete_stats, db.athletes, db.teams).select_from(
        db.athletes.join(db.athlete_stats, isouter=True).join(db.teams, isouter=True)
    ).where(db.athletes.c.athlete_id == id)

    with db.engine.begin() as conn:
        name = conn.execute(athlete).fetchone()

        if not name:
            raise HTTPException(status_code=404, detail="athlete not found.")

        if year:
            athlete = athlete.where(db.athlete_stats.c.year == year)

        athlete = conn.execute(athlete).fetchall()

        if len(athlete) == 0 or not athlete[0].year:
            stats = []
        else:
            stats = [{
                "year": row.year,
                "age": row.age,
                "team_id": row.team_id,
                "team_name": row.team_name,
                "games_played": row.games_played,
                "minutes_played": row.minutes_played,
                "field_goal_percentage": row.field_goal_percentage,
                "free_throw_percentage": row.free_throw_percentage,
                "total_rebounds": row.total_rebounds,
                "assists": row.assists,
                "steals": row.steals,
                "blocks": row.blocks,
                "turnovers": row.turnovers,
                "points": row.points
            }
                for row in athlete]

        json = {
            "athlete_id": id,
            "name": name.name,
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
    turnovers = "turnovers"
    points = "points"


@router.get("/athletes/compare_athletes/", tags=["athletes"])
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
    If the stat is none, then the athlete has no data for the given year.
    """
    if not (2019 <= year <= 2023):
        raise HTTPException(status_code=400, detail="please enter a year within 2019 to 2023 (inclusive)")

    if not athlete_ids or len(athlete_ids) < 2:
        raise HTTPException(status_code=400, detail="athlete list given does not contain enough athletes.")

    athlete_stats = sqlalchemy.select(db.athlete_stats, db.athletes).select_from(
        db.athletes.join(db.athlete_stats, isouter=True)
    ).where(
        (db.athletes.c.athlete_id.in_(athlete_ids) & (db.athlete_stats.c.year == year))
    ).order_by(
        sqlalchemy.desc(sqlalchemy.column(stat)))

    with db.engine.begin() as conn:
        result = conn.execute(athlete_stats).fetchall()

        json = [
            {
                "athlete_id": row.athlete_id,
                "name": row.name,
                stat.value: getattr(row, stat)
            }
            for row in result]

        included_ids = [athlete.get("athlete_id") for athlete in json]
        excluded_ids = [x for x in athlete_ids if x not in included_ids]

        excluded_athletes_stmt = sqlalchemy.select(db.athletes.c.athlete_id, db.athletes.c.name).where(sqlalchemy.column('athlete_id').in_(excluded_ids))
        excluded_names = conn.execute(excluded_athletes_stmt).fetchall()

        for row in excluded_names:
            json.append(
                {
                    "athlete_id": row.athlete_id,
                    "name": row.name,
                    stat.value: None
                }
            )
    return json
@router.get("/athletes/list_athletes/", tags=["athletes"])
def list_athletes(name: str = "",
            limit: int = Query(250, ge=1, le=250),
            offset: int = Query(0, ge=0)
            ):
    """
    This endpoint returns a list of teams. For each team it returns:
    * `team_id`: the internal id of the character. Can be used to query the
    `/teams/{team_id}` endpoint.
    * `team_name`: The name of the team.
    * `team_abbrev`: The abbreviation of the team.

    You can filter for teams whose name contains a string by using the
    `name` query parameter.

    The `limit` and `offset` query
    parameters are used for pagination. The `limit` query parameter specifies the
    maximum number of results to return. The `offset` query parameter specifies the
    number of results to skip before returning results.
    """

    stmt = (
        sqlalchemy.select(
            db.athletes.c.athlete_id,
            db.athletes.c.name
        )
            .limit(limit)
            .offset(offset)
    )

    # filter only if name parameter is passed
    if name != "":
        stmt = stmt.where(db.athletes.c.name.ilike(f"%{name}%"))

    with db.engine.connect() as conn:
        result = conn.execute(stmt)
        json = [{
            "athlete_id": row.athlete_id,
            "athlete name": row.name,
        }
            for row in result]

    return json

@router.post("/athletes/{athlete_name}", tags=["athletes"])
def add_athlete(name: str):
    """
    This endpoint adds an athlete to the database.
    To add stats of a season in which the athlete played, use add_athlete_stats.
    The endpoint returns the id of the resulting athlete that was created
    This endpoint ensures the athlete does not already exist in the database
    * `name` a string of the name of the athlete
    """

    # perform case sensitivity
    name = name.title() 

    potential_athlete_id = sqlalchemy.select(
        db.athletes.c.athlete_id
    ).where(db.athletes.c.name == name)

    with db.engine.begin() as conn:
        result = conn.execute(potential_athlete_id).fetchone()

        if result:
            raise HTTPException(status_code=400, detail="athlete already exists in database")

        athlete_id = conn.execute(
            sqlalchemy.select(
                db.athletes.c.athlete_id
            )
                .order_by(sqlalchemy.desc(db.athletes.c.athlete_id))
                .limit(1)
        ).scalar_one() + 1

        new_athlete = {
            "athlete_id": athlete_id,
            "name": name
        }
        conn.execute(db.athletes.insert().values(**new_athlete))

    return athlete_id


class AthleteStats(BaseModel):
    games_played: int
    minutes_played: int
    field_goal_percentage: float
    free_throw_percentage: float
    total_rebounds: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    points: int


class AthleteJson(BaseModel):
    athlete_id: int
    age: int
    year: int
    team_id: int
    stats: AthleteStats


@router.post("/athletes/season/", tags=["athletes"])
def add_athlete_season(athlete: AthleteJson):
    """
    This endpoint adds the stats from an athlete's season to the database.
    The athlete is represented by the AthleteJson, which contains
    * `athlete_id`: the internal id of the athlete
    * `age`: age of the athlete
    * `year`: year that's being added
    * `team_id`: the team id of the athlete’s team
    * `stats`: a dictionary, matching StatOptions (such as "points") to values

    This endpoint ensures that athlete_id and team_id exists in the database, and that
    the athlete year pair does not already exist in the database
    The endpoint returns the name and year of the athlete
    """

    if not (2019 <= athlete.year <= 2023):
        raise HTTPException(status_code=400, detail="please enter a year within 2019 to 2023 (inclusive)")

    athlete_name_stmt = sqlalchemy.select(db.athletes.c.name).where(db.athletes.c.athlete_id == athlete.athlete_id)

    with db.engine.begin() as conn:
        athlete_name = conn.execute(athlete_name_stmt).fetchone()

        new_athlete_season = {
            "athlete_id": athlete.athlete_id,
            "year": athlete.year,
            "age": athlete.age,
            "team_id": athlete.team_id,
            "games_played": athlete.stats.games_played,
            "minutes_played": athlete.stats.minutes_played,
            "field_goal_percentage": athlete.stats.field_goal_percentage,
            "free_throw_percentage": athlete.stats.free_throw_percentage,
            "total_rebounds": athlete.stats.total_rebounds,
            "assists": athlete.stats.assists,
            "steals": athlete.stats.steals,
            "blocks": athlete.stats.blocks,
            "turnovers": athlete.stats.turnovers,
            "points": athlete.stats.points
        }

        try:
            conn.execute(db.athlete_stats.insert().values(**new_athlete_season))
        except IntegrityError as integrity_error:
            error_message = str(integrity_error)
            start_index = error_message.find('constraint') + len('constraint') + 2
            end_index = error_message.find('Key', start_index) - 11
            constraint_name = error_message[start_index:end_index].strip()
            raise HTTPException(status_code=404, detail="Constraint violated: " + str(constraint_name))

        refresh_max_athletes = sqlalchemy.text('''
        REFRESH MATERIALIZED VIEW max_athlete_stats;
        ''')
        conn.execute(refresh_max_athletes)

    return f"{athlete_name.name}: {athlete.year}"


