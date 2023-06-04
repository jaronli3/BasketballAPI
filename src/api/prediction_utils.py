def get_predictions(stats_json, metadata, year_type):
    x_train = [season.get(year_type) for season in stats_json]
    predictions = {}
    for key in stats_json[0].keys():
        if key not in metadata:
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

def calc_team_market_price(team_stats_json, ratings):
    teams_metadata = ["season", "losses"]

    max_values = {
        "wins": 82,
        "average points for": 150,
        "average points allowed": 150
    }

    predictions = get_predictions(team_stats_json, teams_metadata, "season")

    norm_predictions = normalize_predictions(predictions, max_values)

    ratings_sum = sum(ratings)
    ratings_count = len(ratings)
    mean_rating = ratings_sum / ratings_count if ratings_count > 0 else 3  # Average

    # Output
    weights = {
        "wins": 0.7,
        "average points for": 0.7,
        "average points allowed": -0.4
    }

    market_price = calculate_mp(weights, norm_predictions, mean_rating)
    return round(market_price, 2)

def calc_athlete_market_price(athlete_stats_json, ratings, result):
    athlete_metadata = ["athlete_id", "year", "age", "team_id", "team_name"]

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

    predictions = get_predictions(athlete_stats_json, athlete_metadata, "year")    

    norm_predictions = normalize_predictions(predictions, max_values)

    ratings = [rating_instance.rating for rating_instance in ratings]

    ratings_sum = sum(ratings)
    ratings_count = len(ratings)
    mean_rating = ratings_sum / ratings_count if ratings_count > 0 else 3 

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
