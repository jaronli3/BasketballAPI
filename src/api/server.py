from fastapi import FastAPI
from src.api import athletes

description = """
Group project description 
"""

tags_metadata = [
    {
        "name": "athletes",
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
app.include_router(athletes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the GROUP PROJECT here!. See /docs for more information."}
