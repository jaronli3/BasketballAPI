from fastapi import APIRouter, HTTPException
import sqlalchemy
from sqlalchemy import inspect

from src import database as db
from src.api.teams import team_options
from src.api import athletes, teams
from scipy import array, average
from sklearn.linear_model import LinearRegression

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

    # Predictions
    athlete_stats_json = athletes.get_athlete(id).get("stats")

    if len(athlete_stats_json) == 0:
        raise HTTPException(status_code=400, detail="athlete has no data associated with them")

    athlete_metadata = ["athlete_id", "year", "age", "team_id", "team_name"]

    x_train = array([season.get("year") for season in athlete_stats_json]).reshape(-1, 1)
    predictions = {}
    for key in athlete_stats_json[0].keys():
        if key not in athlete_metadata:
            y_train = array([season.get(key) for season in athlete_stats_json])
            model = LinearRegression()
            model.fit(x_train, y_train)
            prediction = model.predict([[2024]])
            predictions[key] = prediction[0]

    # Max values
    inspector = inspect(db.engine)
    columns = inspector.get_columns("athlete_stats")

    max_values = {}
    with db.engine.connect() as conn:
        for column in columns:
            column_name = column['name']
            if column_name not in athlete_metadata:
                query = sqlalchemy.text(f'SELECT MAX({column_name}) FROM athlete_stats')
                result = conn.execute(query)
                max_value = result.scalar()
                max_values[column_name] = max_value

    std_predictions = {}
    for key in max_values.keys():
        pred = predictions.get(key)
        max_val = max_values.get(key)
        if pred and max_val and max_val != 0:
            std_predictions[key] = pred / max_val

    # Ratings
    ratings_stmt = sqlalchemy.select(db.athlete_ratings.c.rating).where(db.athlete_ratings.c.athlete_id == id)
    with db.engine.begin() as conn:
        ratings = conn.execute(ratings_stmt).fetchall()

    mean_rating = average(ratings) if len(ratings) > 0 else 3  # Average

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
    print(weighted_sum)
    print(mean_rating)
    return round(market_price, 2)


print(get_athlete_market_price(107))
