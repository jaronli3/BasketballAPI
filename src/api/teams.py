from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
import sqlalchemy
from fastapi.params import Query
from src import database as db
from typing import List, Dict

router = APIRouter()

@router.get("/teams/{id}", tags=["teams"])

def get_team(team_id: int):

    ''' 
    This endpoint returns a single team by its identifier. For each team it returns:
        team_id: The internal id of the team
        team_name: The name of the team
        Wins: Number of games the team won
        Losses: Number of games the team lost
        Average Points for: Average number of points the team scored
        Average Points allowed: Average number of points team allowed
    '''

    team = sqlalchemy.select(db.teams.c.team_id, db.teams.c.team_name, db.teams.c.team_abbrev).where(db.teams.c.team_id == team_id)

    with db.engine.connect() as conn:
        result = conn.execute(team).fetchone()
        if result:
            json = {"team_id": team_id, "team_name": result.team_name}
            games = sqlalchemy.select(db.games.c.home, 
                                    db.games.c.away, 
                                    db.games.c.pts_home, 
                                    db.games.c.pts_away, 
                                    db.games.c.winner).where((team_id == db.games.c.home) | (team_id == db.games.c.away))

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
    # avg_fg_pct = "average field goal percentage"
    avg_3p_pct = "average three point percentage"
    # avg_ft_pct = "average free throw percentage"

@router.get("/teams/", tags=["teams"])
def compare_team(teams: List[str] = Query(None), compare_by: stat_options = stat_options.wins):

    ''' 
    This endpoint compares any number of teams (> 1) by a single metric 
        * 'Team_names': list of team names (length > 1) 
        * Compare_by must be one of the following values 
            * "wins"
            * "points"
            * "rebounds"
            * "assists"
            * "steals"
            * "blocks"
            * "average three point percentage"
    '''


    if len(teams) < 2:
        raise HTTPException(status_code=400, detail="not enough teams given")
    
    stmt = (
        sqlalchemy.select(db.teams.c.team_id, db.teams.c.team_name)
        .where(sqlalchemy.column('team_name').in_(teams))
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
                                    db.games.c.three_p_percent_home,
                                    db.games.c.away, 
                                    db.games.c.pts_away, 
                                    db.games.c.winner,
                                    db.games.c.reb_away,
                                    db.games.c.ast_away,
                                    db.games.c.stl_away,
                                    db.games.c.blk_away,
                                    db.games.c.three_p_percent_away).where((row.team_id == db.games.c.home) | (row.team_id == db.games.c.away))

            games1 = conn.execute(games).fetchall()
            wins = 0
            points = 0
            rebounds = 0 
            assists = 0
            steals = 0
            blocks = 0
            average_three = 0

            for game in games1:
                if game.winner == row.team_id:
                    wins += 1
                if game.home == row.team_id:
                    points += game.pts_home
                    rebounds += game.reb_home
                    assists += game.ast_home
                    steals += game.stl_home
                    blocks += game.blk_home
                    average_three += game.three_p_percent_home
                elif game.away == row.team_id:
                    points += game.pts_away
                    rebounds += game.reb_away
                    assists += game.ast_away
                    steals += game.stl_away
                    blocks += game.blk_away
                    average_three += game.three_p_percent_away

            if compare_by == "wins":
                stats_dict = {"Wins": wins}
            elif compare_by == "points":
                stats_dict = {"Average points per game": round((points/82), 2)}
            elif compare_by == "rebounds":
                stats_dict = {"Average rebounds per game": round((rebounds/82), 2)}
            elif compare_by == "assists":
                stats_dict = { "Average assists per game": round((assists/82),2)}
            elif compare_by == "steals":
                stats_dict = { "Average steals per game": round((steals/82), 2)}
            elif compare_by == "blocks":
                stats_dict = {  "Average blocks per game": round((blocks/82), 2)}
            elif compare_by == "average three point percentage":
                stats_dict = {"Average three point percentage per game": round((average_three/82), 2)}
            
            team_dict[f"Compare by {compare_by}"] = stats_dict

            json.append(team_dict)
        
        return json