import random
from src.database import engine


def fake_team_rating():
    ratings = [{"team_rating_id": i, "team_id": random.randint(0, 29), "rating": random.randint(1, 5)} for i in range(1000000)]
    return ratings


print(fake_team_rating())
