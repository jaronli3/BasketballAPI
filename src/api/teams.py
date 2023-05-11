from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
import sqlalchemy
from fastapi.params import Query
from src import database as db
from typing import List, Dict
import operator


router = APIRouter()

class team_options(str, Enum):
    toronto_raptors = "Toronto Raptors"
    memphis_grizzlies = "Memphis Grizzlies"
    miami_heat = "Miami Heat"
    utah_jazz = "Utah Jazz"
    milwaukee_bucks = "Milwaukee Bucks"
    cleveland_cavaliers = "Cleveland Cavaliers"
    new_orleans_pelicans = "New Orleans Pelicans"
    minnesota_timberwolves = "Minnesota Timberwolves"
    orlando_magic = "Orlando Magic"
    new_york_knicks = "New York Knicks"
    washington_wizards = "Washington Wizards"
    phoenix_suns = "Phoenix Suns"
    detroit_pistons = "Detroit Pistons"
    golden_state_warriors = "Golden State Warriors"
    charlotte_hornets = "Charlotte Hornets"
    san_antonio_spurs = "San Antonio Spurs"
    sacramento_kings = "Sacramento Kings"
    los_angeles_clippers = "Los Angeles Clippers"
    oklahoma_city_thunder = "Oklahoma City Thunder"
    dallas_mavericks = "Dallas Mavericks"
    los_angeles_lakers = "Los Angeles Lakers"
    indiana_pacers = "Indiana Pacers"
    atlanta_hawks = "Atlanta Hawks"
    chicago_bulls = "Chicago Bulls"
    denver_nuggets = "Denver Nuggets"
    boston_celtics = "Boston Celtics"
    portland_trail_blazers = "Portland Trail Blazers"
    philadelphia_76ers = "Philadelphia 76ers"
    houston_rockets = "Houston Rockets"
    brooklyn_nets = "Brooklyn Nets"

@router.get("/teams/{team_id}", tags=["teams"])
def get_team(team_id: int):
    """
    This endpoint returns a single team by its identifier. For each team it returns:
        *`team_id`: The internal id of the team
        *`team_name`: The name of the team
        *`Wins`: Number of games the team won
        *`Losses`: Number of games the team lost
        *`Average Points for`: Average number of points the team scored
        *`Average Points allowed`: Average number of points team allowed
    """

    team = sqlalchemy.select(db.teams.c.team_id, db.teams.c.team_name, db.teams.c.team_abbrev).where(
        db.teams.c.team_id == team_id)

    with db.engine.connect() as conn:
        result = conn.execute(team).fetchone()
        if result:
            json = {"team_id": team_id, "team_name": result.team_name}
            games = sqlalchemy.select(db.games.c.home,
                                      db.games.c.away,
                                      db.games.c.pts_home,
                                      db.games.c.pts_away,
                                      db.games.c.winner).where(
                (team_id == db.games.c.home) | (team_id == db.games.c.away))

            games_table = conn.execute(games).fetchall()

            wins = 0
            points_for = 0
            points_allowed = 0

            for row in games_table:
                if row.winner == team_id:
                    wins += 1
                if team_id == row.home:
                    points_for += row.pts_home
                    points_allowed += row.pts_away
                elif team_id == row.away:
                    points_for += row.pts_away
                    points_allowed += row.pts_home

            json["Wins"] = wins
            json["Losses"] = 82 - wins
            json["Average Points For"] = round((points_for / 82), 2)
            json["Average Points Allowed"] = round((points_allowed / 82), 2)

            return json

        raise HTTPException(status_code=404, detail="team not found.")


class stat_options(str, Enum):
    wins = "wins"
    points = "points"
    rebounds = "rebounds"
    assists = "assists"
    steals = "steals"
    blocks = "blocks"


@router.get("/teams/", tags=["teams"])
def compare_team(team_1: team_options,
                 team_2: team_options,
                 team_3: team_options = None,
                 team_4: team_options = None,
                 team_5: team_options = None,
                 compare_by: stat_options = stat_options.wins):
    '''
    This endpoint compares between 2 and 5 teams by a single metric
        * 'team_i': a team to be compared
        * Compare_by must be one of the following values 
            * `wins`: The average wins per season
            * `points`: The average points per game
            * `rebounds`: The average rebounds per game
            * `assists`: The average assists per game
            * `steals`: The average steals per game
            * `blocks`: The average blocks per game
    '''

    stmt = (
        sqlalchemy.select(db.teams.c.team_id, db.teams.c.team_name)
            .where(sqlalchemy.column('team_name').in_([team_1, team_2, team_3, team_4, team_5]))
    )

    with db.engine.connect() as conn:
        result = conn.execute(stmt).fetchall()
        json = []
        for row in result:
            team_dict = {"team id": row.team_id, "team name": row.team_name}
            games = sqlalchemy.select(db.games.c.home,
                                      db.games.c.pts_home,
                                      db.games.c.winner,
                                      db.games.c.reb_home,
                                      db.games.c.ast_home,
                                      db.games.c.stl_home,
                                      db.games.c.blk_home,
                                      db.games.c.away,
                                      db.games.c.pts_away,
                                      db.games.c.winner,
                                      db.games.c.reb_away,
                                      db.games.c.ast_away,
                                      db.games.c.stl_away,
                                      db.games.c.blk_away).where(
                (row.team_id == db.games.c.home) | (row.team_id == db.games.c.away))

            games1 = conn.execute(games).fetchall()
            wins = 0
            points = 0
            rebounds = 0
            assists = 0
            steals = 0
            blocks = 0

            for game in games1:
                if game.winner == row.team_id:
                    wins += 1
                if game.home == row.team_id:
                    points += game.pts_home
                    rebounds += game.reb_home
                    assists += game.ast_home
                    steals += game.stl_home
                    blocks += game.blk_home
                elif game.away == row.team_id:
                    points += game.pts_away
                    rebounds += game.reb_away
                    assists += game.ast_away
                    steals += game.stl_away
                    blocks += game.blk_away

            if compare_by == "wins":
                metric = wins / 5
            elif compare_by == "points":
                metric = round((points / (82*5)), 2)
            elif compare_by == "rebounds":
                metric = round((rebounds / (82*5)), 2)
            elif compare_by == "assists":
                metric = round((assists / (82*5)), 2)
            elif compare_by == "steals":
                metric = round((steals / (82*5)), 2)
            elif compare_by == "blocks":
                metric = round((blocks / (82*5)), 2)

            team_dict[str(compare_by.value)] = metric
            json.append(team_dict)

            json.sort(key=lambda x: -x[compare_by])

        return json
