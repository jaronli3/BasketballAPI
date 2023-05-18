from fastapi import APIRouter
import sqlalchemy
from src import database as db
from src.api.teams import team_options


router = APIRouter()


@router.get("/predictions/team", tags=["predictions"])
def get_team_market_price(team: team_options):
    """
    This endpoint returns the current market price of the specified team
    """


@router.get("/predictions/athlete", tags=["predictions"])
def get_athlete_market_price(athlete: str):
    """
    This endpoint returns the current market price of the specified athlete
    """