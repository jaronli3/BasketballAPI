from fastapi import APIRouter, HTTPException
import sqlalchemy
from sqlalchemy import inspect

from src import database as db
from src.api.teams import team_options
from src.api import athletes, teams
import time

router = APIRouter()


@router.get("/predictions/team", tags=["predictions"])
def get_team_market_price(team: team_options):
    """
    This endpoint returns the current market price of the specified team
    """
    team_stats_json = teams.get_team(team)
    print(team_stats_json)


# print(get_team_market_price(team_options.toronto_raptors))

@router.get("/predictions/athlete", tags=["predictions"])
def get_athlete_market_price(id: int):
    """
    This endpoint returns the current market price of the specified athlete
    """
    start = time.time()

    # Predictions
    athlete_stats_json = athletes.get_athlete(id).get("stats")

    if len(athlete_stats_json) == 0:
        raise HTTPException(status_code=400, detail="athlete has no data associated with them")

    athlete_metadata = ["athlete_id", "year", "age", "team_id", "team_name"]

    x_train = [season.get("year") for season in athlete_stats_json]
    predictions = {}
    print(time.time()-start)
    for key in athlete_stats_json[0].keys():
        if key not in athlete_metadata:
            y_train = [season.get(key) for season in athlete_stats_json]
            x_mean = sum(x_train) / len(x_train)
            y_mean = sum(y_train) / len(y_train)
            numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_train, y_train))
            denominator = sum((x - x_mean) ** 2 for x in x_train)
            slope = numerator / denominator
            intercept = y_mean - (slope * x_mean)
            prediction = intercept + slope * 2024
            predictions[key] = prediction
    print(time.time() - start)
    # Max values
    # inspector = inspect(db.engine)
    # columns = inspector.get_columns("athlete_stats")
    #
    # max_values = {}
    # with db.engine.connect() as conn:
    #     for column in columns:
    #         column_name = column['name']
    #         if column_name not in athlete_metadata:
    #             query = sqlalchemy.text(f'SELECT MAX({column_name}) FROM athlete_stats')
    #             result = conn.execute(query)
    #             max_value = result.scalar()
    #             max_values[column_name] = max_value

    stmt = sqlalchemy.select(db.max_athlete_stats)
    with db.engine.begin() as conn:
        result = conn.execute(stmt).fetchone()
    print(result)
    max_values = {
        "games_played": result.max_games_played,
        "minutes_played": result.max_minutes_played,
        "field_goal_percentage": result.max_field_goal_percentage,
        "free_throw_percentage": result.max_free_throw_percentage,
        "total_rebounds": result.max_total_rebounds,
        "assists": result.max_assists,
        "steals": result.max_steals,
        "blocks": result.max_blocks,
        "turnovers": result.max_turnovers,
        "points": result.max_points
    }

    print(max_values)

    print(time.time() - start)
    std_predictions = {}
    for key in max_values.keys():
        pred = predictions.get(key)
        max_val = max_values.get(key)
        if pred and max_val and max_val != 0:
            std_predictions[key] = pred / max_val
    print(time.time() - start)
    # Ratings
    ratings_stmt = sqlalchemy.select(db.athlete_ratings.c.rating).where(db.athlete_ratings.c.athlete_id == id)
    with db.engine.begin() as conn:
        ratings = conn.execute(ratings_stmt).fetchall()

    ratings = [rating_instance.rating for rating_instance in ratings]

    ratings_sum = sum(ratings)
    ratings_count = len(ratings)
    mean_rating = ratings_sum / ratings_count if ratings_count > 0 else 3  # Average
    print(time.time() - start)
    # Output

    weights = {
        'games_played': 0.2,
        'minutes_played': 0.15,
        'field_goal_percentage': 0.1,
        'free_throw_percentage': 0.1,
        'total_rebounds': 0.08,
        'assists': 0.12,
        'steals': 0.08,
        'blocks': 0.03,
        'turnovers': 0.02,
        'points': 0.12
    }

    weighted_sum = sum(std_predictions[prediction] * weights[prediction] for prediction in std_predictions)
    market_price = pow(1 + weighted_sum, mean_rating)
    print(time.time() - start)
    return round(market_price, 2)


print(get_athlete_market_price(107))
