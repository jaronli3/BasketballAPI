import random
from datetime import date, timedelta

import sqlalchemy
import os
import dotenv
from faker import Faker
import numpy as np


def database_connection_url():
    # return "postgresql://postgres:postgres@localhost:54322/postgres"

    dotenv.load_dotenv()
    DB_USER: str = os.environ.get("POSTGRES_USER")
    DB_PASSWD = os.environ.get("POSTGRES_PASSWORD")
    DB_SERVER: str = os.environ.get("POSTGRES_SERVER")
    DB_PORT: str = os.environ.get("POSTGRES_PORT")
    DB_NAME: str = os.environ.get("POSTGRES_DB")
    return f"postgresql://{DB_USER}:{DB_PASSWD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"


# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(database_connection_url(), use_insertmanyvalues=True)

with engine.begin() as conn:
    conn.execute(sqlalchemy.text("""
    DROP TABLE IF EXISTS athlete_ratings;
    DROP TABLE IF EXISTS athlete_stats;
    DROP TABLE IF EXISTS athletes;
    DROP TABLE IF EXISTS games;
    DROP TABLE IF EXISTS team_ratings;
    DROP TABLE IF EXISTS users;

    CREATE TABLE athletes (
        athlete_id serial PRIMARY KEY,
        name text NOT NULL
    );

    CREATE TABLE athlete_stats (
        athlete_id INT NOT NULL,
        year INT NOT NULL,
        age INT NOT NULL,
        team_id INT NOT NULL,
        games_played INT NOT NULL,
        minutes_played INT NOT NULL,
        field_goal_percentage FLOAT NOT NULL,
        free_throw_percentage FLOAT NOT NULL,
        total_rebounds INT NOT NULL,
        assists INT NOT NULL,
        steals INT NOT NULL,
        blocks INT NOT NULL,
        turnovers INT NOT NULL,
        points INT NOT NULL,
        PRIMARY KEY (athlete_id, year),
        FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id),
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
    );

    CREATE TABLE games (
        game_id serial PRIMARY KEY,
        home INT NOT NULL,
        away INT NOT NULL,
        date DATE NOT NULL,
        pts_home INT NOT NULL,
        pts_away INT NOT NULL,
        reb_home INT NOT NULL,
        reb_away INT NOT NULL,
        ast_home INT NOT NULL,
        ast_away INT NOT NULL,
        stl_home INT NOT NULL,
        stl_away INT NOT NULL,
        blk_home INT NOT NULL,
        blk_away INT NOT NULL,
        FOREIGN KEY (home) REFERENCES teams(team_id),
        FOREIGN KEY (away) REFERENCES teams(team_id)
    );

    CREATE TABLE users (
        user_id serial PRIMARY KEY,
        username text NOT NULL,
        hashed_password text NOT NULL
    );

    CREATE TABLE team_ratings (
        team_rating_id serial PRIMARY KEY,
        team_id INT NOT NULL,
        rating INT NOT NULL,
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
    );

    CREATE TABLE athlete_ratings (
        athlete_rating_id serial PRIMARY KEY,
        athlete_id INT NOT NULL,
        rating INT NOT NULL,
        FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id)
    );
    """))
print("Created tables")

fake = Faker()
with engine.begin() as conn:
    num_athletes = 100000
    athletes = []
    for i in range(num_athletes):
        name = fake.name()
        athletes.append(
            {"athlete_id": i,
             "name": name}
        )
    if athletes:
        conn.execute(sqlalchemy.text("""
        INSERT INTO athletes (athlete_id, name)
        VALUES (:athlete_id, :name);
        """), athletes)
    print("Completed athletes")

    athlete_stats = []
    for athlete_id in range(num_athletes):
        birthyear = random.randint(1975, 2000)
        for year in range(2019, 2024):
            athlete_stats.append(
                {
                    "athlete_id": athlete_id,
                    "year": year,
                    "age": year - birthyear,
                    "team_id": random.randint(0, 29),
                    "games_played": random.randint(0, 100),
                    "minutes_played": random.randint(0, 5000),
                    "field_goal_percentage": round(random.random(), 3),
                    "free_throw_percentage": round(random.random(), 3),
                    "total_rebounds": random.randint(0, 1000),
                    "assists": random.randint(0, 100),
                    "steals": random.randint(0, 100),
                    "blocks": random.randint(0, 500),
                    "turnovers": random.randint(0, 500),
                    "points": random.randint(0, 5000)
                }
            )
    if athlete_stats:
        conn.execute(sqlalchemy.text("""
        INSERT INTO athlete_stats (athlete_id, year, age, team_id, games_played, minutes_played, field_goal_percentage,
        free_throw_percentage, total_rebounds, assists, steals, blocks, turnovers, points)
        VALUES (:athlete_id, :year, :age, :team_id, :games_played, :minutes_played, :field_goal_percentage,
        :free_throw_percentage, :total_rebounds, :assists, :steals, :blocks, :turnovers, :points);
        """), athlete_stats)
    print("Completed athlete_stats")

    num_games = 100000
    games = []
    for i in range(num_games):
        teams = random.sample(range(30), 2)

        start_date = date(2019, 1, 1)
        end_date = date(2023, 4, 30)
        time_between_dates = end_date - start_date
        random_number_of_days = random.randrange(time_between_dates.days)
        random_date = start_date + timedelta(days=random_number_of_days)

        points = random.sample(range(170), 2)

        games.append(
            {
                "game_id": i,
                "home": teams[0],
                "away": teams[1],
                "date": random_date,
                "pts_home": points[0],
                "pts_away": points[1],
                "reb_home": random.randint(0, 70),
                "reb_away": random.randint(0, 70),
                "ast_home": random.randint(0, 70),
                "ast_away": random.randint(0, 70),
                "stl_home": random.randint(0, 20),
                "stl_away": random.randint(0, 20),
                "blk_home": random.randint(0, 20),
                "blk_away": random.randint(0, 20)
            }
        )
    if games:
        conn.execute(sqlalchemy.text("""
        INSERT INTO games (game_id, home, away, date, pts_home, pts_away, reb_home, reb_away, ast_home, ast_away,
        stl_home, stl_away, blk_home, blk_away)
        VALUES (:game_id, :home, :away, :date, :pts_home, :pts_away, :reb_home, :reb_away, :ast_home, :ast_away,
        :stl_home, :stl_away, :blk_home, :blk_away);
        """), games)
    print("Completed games")

    num_athlete_ratings = 150000
    athlete_ratings = []
    for i in range(num_athlete_ratings):
        athlete_ratings.append(
            {
                "athlete_rating_id": i,
                "athlete_id": random.randint(0, num_athletes - 1),
                "rating": random.randint(1, 5)
            }
        )
    if athlete_ratings:
        conn.execute(sqlalchemy.text("""
        INSERT INTO athlete_ratings (athlete_rating_id, athlete_id, rating)
        VALUES (:athlete_rating_id, :athlete_id, :rating);
        """), athlete_ratings)
    print("Completed athlete_ratings")

    num_team_ratings = 150000
    team_ratings = []
    for i in range(num_team_ratings):
        team_ratings.append(
            {
                "team_rating_id": i,
                "team_id": random.randint(0, 29),
                "rating": random.randint(1, 5)
            }
        )
    if team_ratings:
        conn.execute(sqlalchemy.text("""
        INSERT INTO team_ratings (team_rating_id, team_id, rating)
        VALUES (:team_rating_id, :team_id, :rating);
        """), team_ratings)
    print("Completed team_ratings")

with engine.begin() as conn:
    conn.execute(
        sqlalchemy.text("""
            DROP MATERIALIZED VIEW IF EXISTS max_athlete_stats;

            CREATE MATERIALIZED VIEW max_athlete_stats AS
                SELECT MAX(games_played) AS max_games_played, MAX(minutes_played) AS max_minutes_played, 
                MAX(field_goal_percentage) AS max_field_goal_percentage, 
                MAX(free_throw_percentage) AS max_free_throw_percentage, 
                MAX(total_rebounds) AS max_total_rebounds, 
                MAX(assists) AS max_assists, 
                MAX(steals) AS max_steals, 
                MAX(blocks) AS max_blocks, 
                MAX(turnovers) AS max_turnovers, 
                MAX(points) AS max_points
        FROM athlete_stats;
        """)
    )
    print("Completed materialized_view")

