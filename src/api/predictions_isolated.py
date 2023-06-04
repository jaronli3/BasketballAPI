from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


def get_predictions(stats_json):
    x_train = [season.get("season") for season in stats_json]
    predictions = {}
    for key in stats_json[0].keys():
        if key != "season":
            y_train = [season.get(key) for season in stats_json]
            x_mean = sum(x_train) / len(x_train)
            y_mean = sum(y_train) / len(y_train)
            numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_train, y_train))
            denominator = sum((x - x_mean) ** 2 for x in x_train)
            slope = numerator / denominator
            intercept = y_mean - (slope * x_mean)
            prediction = intercept + slope * 2024
            predictions[key] = prediction
    return predictions


def normalize_predictions(predictions, max_values):
    norm_predictions = {}
    for key in max_values.keys():
        pred = predictions.get(key)
        max_val = max_values.get(key)
        if pred and max_val and max_val != 0:
            norm_predictions[key] = pred / max_val
        else:
            norm_predictions[key] = 0
    return norm_predictions


def calculate_mp(weights, norm_predictions, mean_rating):
    weighted_sum = sum(norm_predictions[prediction] * weights[prediction] for prediction in norm_predictions)
    market_price = pow(1 + weighted_sum, mean_rating)
    return market_price


class TeamSeason(BaseModel):
    wins: int
    average_points_for: int
    average_points_allowed: int


class TeamJson(BaseModel):
    stats_2019: TeamSeason
    stats_2020: TeamSeason
    stats_2021: TeamSeason
    stats_2022: TeamSeason
    stats_2023: TeamSeason


@router.post("/predictions_isolated/team", tags=["predictions_isolated"])
def get_team_market_price(team_stats: TeamJson,
                          mean_rating: int):
    """
    This endpoint returns the current market price of the specified team
    """

    team_stats_json = [
        {
            "season": year,
            "wins": getattr(team_stats, "stats_" + str(year)).wins,
            "average points for": getattr(team_stats, "stats_" + str(year)).average_points_for,
            "average points allowed": getattr(team_stats, "stats_" + str(year)).average_points_allowed,
        }
        for year in range(2019, 2024)]

    predictions = get_predictions(team_stats_json)

    max_values = {
        "wins": 82,
        "average points for": 150,
        "average points allowed": 150
    }

    norm_predictions = normalize_predictions(predictions, max_values)

    weights = {
        "wins": 0.7,
        "average points for": 0.7,
        "average points allowed": -0.4
    }

    market_price = calculate_mp(weights, norm_predictions, mean_rating)
    return round(market_price, 2)


class AthleteSeason(BaseModel):
    games_played: int
    minutes_played: int
    field_goal_percentage: float
    free_throw_percentage: float
    total_rebounds: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    points: int


class AthleteJson(BaseModel):
    stats_2019: AthleteSeason
    stats_2020: AthleteSeason
    stats_2021: AthleteSeason
    stats_2022: AthleteSeason
    stats_2023: AthleteSeason


@router.post("/predictions_isolated/athlete", tags=["predictions_isolated"])
def get_athlete_market_price(athlete_stats: AthleteJson,
                             mean_rating: int):
    """
    This endpoint returns the current market price of the specified athlete
    * `id` the id of the athlete 
    """

    # Predictions
    athlete_stats_json = [
        {
            "season": year,
            "games_played": getattr(athlete_stats, "stats_" + str(year)).games_played,
            "minutes_played": getattr(athlete_stats, "stats_" + str(year)).minutes_played,
            "field_goal_percentage": getattr(athlete_stats, "stats_" + str(year)).field_goal_percentage,
            "free_throw_percentage": getattr(athlete_stats, "stats_" + str(year)).free_throw_percentage,
            "total_rebounds": getattr(athlete_stats, "stats_" + str(year)).total_rebounds,
            "assists": getattr(athlete_stats, "stats_" + str(year)).assists,
            "steals": getattr(athlete_stats, "stats_" + str(year)).steals,
            "blocks": getattr(athlete_stats, "stats_" + str(year)).blocks,
            "turnovers": getattr(athlete_stats, "stats_" + str(year)).turnovers,
            "points": getattr(athlete_stats, "stats_" + str(year)).points
        }
        for year in range(2019, 2024)]

    predictions = get_predictions(athlete_stats_json)

    max_values = {
        "games_played": 82,
        "minutes_played": 3028,
        "field_goal_percentage": 1.0,
        "free_throw_percentage": 1.0,
        "total_rebounds": 1232,
        "assists": 784,
        "steals": 170,
        "blocks": 199,
        "turnovers": 387,
        "points": 2818
    }

    norm_predictions = normalize_predictions(predictions, max_values)

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

    market_price = calculate_mp(weights, norm_predictions, mean_rating)
    return round(market_price, 2)
