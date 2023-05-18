from fastapi import APIRouter
import sqlalchemy
from src import database as db
from src.api.teams import team_options
# from fastapi.testclient import TestClient
# from src.api.server import app
#
#
# client = TestClient(app)

router = APIRouter()


@router.get("/predictions/team", tags=["predictions"])
def get_team_market_price(team: team_options):
    """
    This endpoint returns the current market price of the specified team
    """


print(get_team_market_price(team_options.toronto_raptors))

@router.get("/predictions/athlete", tags=["predictions"])
def get_athlete_market_price(athlete: str):
    """
    This endpoint returns the current market price of the specified athlete
    """