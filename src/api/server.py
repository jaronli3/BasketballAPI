from fastapi import FastAPI
# from src.api import *

description = """
Group project description 
"""

tags_metadata = [
    {
        "name": "players",
        "description": "Access player information.",
    },
]

app = FastAPI(
    title="Temporary Title",
    description=description,
    version="0.0.1",
    contact={
        "name": "Quinn Peterson",
        "email": "qpeterso@calpoly.edu",
    },
    openapi_tags=tags_metadata,
)
# app.include_router(characters.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the GROUP PROJECT. See /docs for more information."}
