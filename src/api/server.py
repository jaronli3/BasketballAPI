from fastapi import FastAPI
from src.api import athletes, games, teams, pkg_util, ratings, login, predictions

description = """
Get all the information and analytical insight 
you need about the NBA regular season from 2019 through 2023.
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
    },
    {
        "name": "ratings",
        "description": "Rate teams and athletes.",
    },
    {
        "name": "predictions",
        "description": "Get market values for athletes and teams.",
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
app.include_router(ratings.router)
app.include_router(login.router)
app.include_router(predictions.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Basketball API here!. See /docs for more information."}
