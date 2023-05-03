from sqlalchemy import create_engine
import os
import dotenv
import sqlalchemy

def database_connection_url():
    dotenv.load_dotenv()
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    return f"postgresql://postgres:{DB_PASSWD}@db.cilwbqbgvckpilzqjarl.supabase.co:6543/postgres"

# Create a new DB engine based on our connection string
engine = create_engine(database_connection_url())

with engine.begin() as conn:
    metadata_obj = sqlalchemy.MetaData()

    athletes = sqlalchemy.Table("athletes", metadata_obj, autoload_with=engine)
