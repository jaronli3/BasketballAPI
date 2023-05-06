from fastapi import FastAPI
from src.api import athletes, games, teams
from src.api import pkg_util

description = """
Get all the information and analytical insight 
you need about the 2023 NBA regular season.
"""

tags_metadata = [
    {
        "name": "athletes",
        "description": "Access player information.",
    },
    {
        "name": "games",
        "description": "Access game information.",
    },
    {
        "name": "teams",
        "description": "Access team information.",
    }
]

app = FastAPI(
    title="Basketball API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Quinn Peterson, Zachary Weinfeld, Jaron Li",
        "email": "qpeterso@calpoly.edu"
    },
    openapi_tags=tags_metadata,
)

app.include_router(athletes.router)
app.include_router(teams.router)
app.include_router(games.router)
app.include_router(pkg_util.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the GROUP PROJECT here!. See /docs for more information."}
