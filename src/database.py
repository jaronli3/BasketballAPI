from sqlalchemy import create_engine
import os
import dotenv
import sqlalchemy

def database_connection_url():
    dotenv.load_dotenv()
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
    # return f"postgresql://postgres:{DB_PASSWD}@db.cilwbqbgvckpilzqjarl.supabase.co:6543/postgres"

# Create a new DB engine based on our connection string
engine = create_engine(database_connection_url())

with engine.begin() as conn:
    metadata_obj = sqlalchemy.MetaData()

    athletes = sqlalchemy.Table("athletes", metadata_obj, autoload_with=engine)
    games = sqlalchemy.Table("games", metadata_obj, autoload_with=engine)
    teams = sqlalchemy.Table("teams", metadata_obj, autoload_with=engine)

