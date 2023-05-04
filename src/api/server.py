from fastapi import FastAPI
from src.api import athletes
from src.api import games
from src.api import teams
from src.api import pkg_util

description = """
Group project description 
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
    title="Temporary Title",
    description=description,
    version="0.0.1",
    contact={
        "name": "Quinn Peterson, Zachary Weinfeld, Jaron Li",
        "email": "qpeterso@calpoly.edu, zweinfel@calpoly.edu, jli213@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)

app.include_router(athletes.router)
# app.include_router(teams.router)
# app.include_router(games.router)
app.include_router(pkg_util.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the GROUP PROJECT here!. See /docs for more information."}
