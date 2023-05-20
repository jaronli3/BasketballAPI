from sqlalchemy import create_engine
import os
import dotenv
import sqlalchemy

def database_connection_url():
    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


# Create a new DB engine based on our connection string
engine = create_engine(database_connection_url())


metadata_obj = sqlalchemy.MetaData()

athletes = sqlalchemy.Table("athletes", metadata_obj, autoload_with=engine)
games = sqlalchemy.Table("games", metadata_obj, autoload_with=engine)
teams = sqlalchemy.Table("teams", metadata_obj, autoload_with=engine)
athlete_stats = sqlalchemy.Table("athlete_stats", metadata_obj, autoload_with=engine)
users = sqlalchemy.Table("users", metadata_obj, autoload_with=engine)
athlete_ratings = sqlalchemy.Table("athlete_ratings", metadata_obj, autoload_with=engine)
team_ratings = sqlalchemy.Table("team_ratings", metadata_obj, autoload_with=engine)
max_athlete_stats = sqlalchemy.Table("max_athlete_stats", metadata_obj, autoload_with=engine)