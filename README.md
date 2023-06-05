**About**
Basketball API is your best view into the past, present, and future of the NBA. Get all the information you need about historical NBA data from the past 5 years, including data about players, teams, games, and more! Rate current athletes and teams. Predict the trajectory of players and teams by getting their market price.

Basketball API can provide you with historical NBA data in many useful forms. Get stats on an individual athlete, compare different athletes based on various statistics, or search for athletes by name. You can also add an athlete and an athlete’s season to the database. Get information on every NBA game from the past 5 years. Basketball API also supports adding new games to the database. Similarly to athletes, get all the information you need on individual teams, compare teams based on various statistics, or search for teams by name. Provide ratings on individual teams and athletes, which are used in assessing their trajectories. The real power of Basketball API comes into play in these projections, where you can get predictions on the relative success of teams and athletes through a market price. Basketball API also supports user logins.

**Getting Started**
Prerequisites (see requirements.txt)
Ensure all dependencies are installed
Installation
Clone the repository
Install the dependencies
Configure a .env file

**API Endpoints**
This API provides the following endpoints:
‘/athletes/{id}’: This endpoint will return a single athlete by its id.
‘/athletes/compare_athletes/’: This endpoint will give a comparison between the specified athletes and will return the athletes’ ids, names, and stat specified in the input.
‘/athletes/list_athletes/”: This endpoint will return a list of athletes.
‘athletes/{athlete_name}’: This endpoint will add an athlete to the database.
‘/athletes/season’: This endpoint will add the stats from an athlete’s season to the database.
‘/games/’: This endpoint will return a list of games by the teams provided ordered by date.
‘/games/add_game’: This endpoint will add a game to the database.
‘/predictions/team’: This endpoint will return the current market price for the given team.
‘/predictions/athlete’: This endpoint will return the current market price for the given athlete.
‘/teamratings/’: This endpoint will add a user-generated team rating to the database.
‘/athleteratings/’ This endpoint will add a user-generated athlete rating to the database.
‘/teams/{team_id}’: This endpoint will return a single team by its id.
‘/teams/compare_teams/’: This endpoint will give a comparison between the specified teams and will return the teams’ names and stat specified in the input.
‘/teams/’: This endpoint will return a list of teams.




