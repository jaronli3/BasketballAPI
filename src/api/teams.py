from fastapi import APIRouter, HTTPException
from enum import Enum
from collections import Counter
import sqlalchemy
from fastapi.params import Query
from src import database as db

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

            games_table = conn.execute(team).fetchall()

            wins = 0
            points_for = 0
            points_allowed = 0

            for row in games_table:
                if games_table.winner == team_id:
                    wins += 1
                if team_id == games_table.home:
                    points_for += games_table.pts_home
                    points_away += games_table.pts_away
                elif team_id == games_table.away:
                    points_for += games_table.pts_away
                    points_away += games_table.points_for


            json["Wins"] = wins
            json["Losses"] = 82 - wins
            json["Average Points For"] = points_for / 82
            json["Average Points Allowed"] = points_allowed / 82

            return json
            
        raise HTTPException(status_code=404, detail="team not found.")
    

class stat_options(str, Enum):
    wins = "wins"
    points = "points"
    rebounds = "rebounds"
    assists = "assists"
    steals = "steals"
    blocks = "blocks"
    avg_fg_pct = "average field goal percentage"
    avg_3p_pct = "average three point percentage"
    avg_ft_pct = "average free throw percentage"

@router.get("/teams/", tags=["movies"])
def compare_team(teams: list, compare_by: stat_options = stat_options.wins):

    ''' 
    This endpoint compares any number of teams (> 1) by a single metric 
        - Team_names: list of team names (length > 1) 
        - Compare_by must be one of the following values 
            - "wins"
            - "points"
            - "rebounds"
            - "assists"
            - "steals"
            - "blocks"
            - "average field goal percentage"
            - "average three point percentage"
            - "average free throw percentage"
    '''

    ...

    