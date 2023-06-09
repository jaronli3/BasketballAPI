"""create tables

Revision ID: 4c15ee86918d
Revises: 
Create Date: 2023-05-16 14:23:22.006404

"""
from alembic import op
import sqlalchemy as sa
import csv

# revision identifiers, used by Alembic.
from sqlalchemy import table, Column, Integer, Text, Float, Date

revision = '4c15ee86918d'
down_revision = None
branch_labels = None
depends_on = None




def upgrade() -> None:

    # Athletes
    op.create_table(
        'athletes',
        sa.Column('athlete_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.Text, nullable=False)
    )

    athletes = table(
        "athletes",
        Column("athlete_id", Integer),
        Column("name", Text)
    )

    with open("data/athletes.csv", mode="r", encoding="utf-8-sig") as csv_file:
        op.bulk_insert(athletes, [row for row in csv.DictReader(csv_file, skipinitialspace=True)])

    # Teams
    op.create_table(
        'teams',
        sa.Column('team_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('team_abbrev', sa.Text, nullable=False),
        sa.Column('team_name', sa.Text, nullable=False)
    )

    teams = table(
        "teams",
        Column("team_id", Integer),
        Column("team_abbrev", Text),
        Column("team_name", Text)
    )

    with open("data/teams.csv", mode="r", encoding="utf-8-sig") as csv_file:
        op.bulk_insert(teams, [row for row in csv.DictReader(csv_file, skipinitialspace=True)])

    # Athlete Stats
    op.create_table(
        'athlete_stats',
        sa.Column('athlete_id', sa.Integer, primary_key=True),
        sa.ForeignKeyConstraint(['athlete_id'], ['athletes.athlete_id']),
        sa.Column('year', sa.Integer, primary_key=True),
        sa.Column('age', sa.Integer, nullable=False),
        sa.Column('team_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['team_id'], ['teams.team_id']),
        sa.Column('games_played', sa.Integer, nullable=False),
        sa.Column('minutes_played', sa.Integer, nullable=False),
        sa.Column('field_goal_percentage', sa.Float, nullable=False),
        sa.Column('free_throw_percentage', sa.Float, nullable=False),
        sa.Column('total_rebounds', sa.Integer, nullable=False),
        sa.Column('assists', sa.Integer, nullable=False),
        sa.Column('steals', sa.Integer, nullable=False),
        sa.Column('blocks', sa.Integer, nullable=False),
        sa.Column('turnovers', sa.Integer, nullable=False),
        sa.Column('points', sa.Integer, nullable=False)
    )

    athlete_stats = table(
        "athlete_stats",
        Column("athlete_id", Integer),
        Column("year", Integer),
        Column("age", Integer),
        Column("team_id", Integer),
        Column("games_played", Integer),
        Column("minutes_played", Integer),
        Column("field_goal_percentage", Float),
        Column("free_throw_percentage", Float),
        Column("total_rebounds", Integer),
        Column("assists", Integer),
        Column("steals", Integer),
        Column("blocks", Integer),
        Column("turnovers", Integer),
        Column("points", Integer)
    )

    with open("data/athlete_stats.csv", mode="r", encoding="utf-8-sig") as csv_file:
        op.bulk_insert(athlete_stats, [row for row in csv.DictReader(csv_file, skipinitialspace=True)])

    # Games
    op.create_table(
        'games',
        sa.Column('game_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('home', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['home'], ['teams.team_id']),
        sa.Column('away', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['away'], ['teams.team_id']),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('pts_home', sa.Integer, nullable=False),
        sa.Column('pts_away', sa.Integer, nullable=False),
        sa.Column('reb_home', sa.Integer, nullable=False),
        sa.Column('reb_away', sa.Integer, nullable=False),
        sa.Column('ast_home', sa.Integer, nullable=False),
        sa.Column('ast_away', sa.Integer, nullable=False),
        sa.Column('stl_home', sa.Integer, nullable=False),
        sa.Column('stl_away', sa.Integer, nullable=False),
        sa.Column('blk_home', sa.Integer, nullable=False),
        sa.Column('blk_away', sa.Integer, nullable=False)
    )

    games = table(
        "games",
        Column("game_id", Integer),
        Column("home", Integer),
        Column("away", Integer),
        Column("date", Date),
        Column("pts_home", Integer),
        Column("pts_away", Integer),
        Column("reb_home", Integer),
        Column("reb_away", Integer),
        Column("ast_home", Integer),
        Column("ast_away", Integer),
        Column("stl_home", Integer),
        Column("stl_away", Integer),
        Column("blk_home", Integer),
        Column("blk_away", Integer),
    )

    with open("data/games.csv", mode="r", encoding="utf-8-sig") as csv_file:
        op.bulk_insert(games, [row for row in csv.DictReader(csv_file, skipinitialspace=True)])

    # Users
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.Text, nullable=False, unique=True),
        sa.Column('hashed_password', sa.Text, nullable=False)
    )

    # Team Ratings
    op.create_table(
        'team_ratings',
        sa.Column('team_rating_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('team_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['team_id'], ['teams.team_id']),
        sa.Column('rating', sa.Integer, nullable=False)
    )

    # Athlete Ratings
    op.create_table(
        'athlete_ratings',
        sa.Column('athlete_rating_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('athlete_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['athlete_id'], ['athletes.athlete_id']),
        sa.Column('rating', sa.Integer, nullable=False)
    )

    create_athlete_view = '''
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
    '''

    op.execute(create_athlete_view)

    # create_user = '''CREATE USER lucaspierce PASSWORD 'professorpierce1234';'''
    #
    # op.execute(create_user)
    #
    # create_role = '''
    # CREATE ROLE read_only;
    # '''
    #
    # op.execute(create_role)
    #
    # grant_user = '''
    # GRANT SELECT ON games TO read_only;
    # GRANT SELECT ON team_ratings TO read_only;
    # GRANT SELECT ON teams TO read_only;
    # GRANT SELECT ON athletes TO read_only;
    # GRANT SELECT ON athlete_ratings TO read_only;
    # GRANT SELECT ON athlete_stats TO read_only;
    # '''
    # op.execute(grant_user)
    #
    # grant_role_to_user = '''
    # GRANT read_only TO lucaspierce;
    # '''
    #
    # op.execute(grant_role_to_user)



def downgrade() -> None:

    # op.execute("DROP ROLE lucaspierce")

    op.execute('DROP MATERIALIZED VIEW max_athlete_stats')

    op.drop_table('athlete_ratings')
    op.drop_table('team_ratings')
    op.drop_table('games')
    op.drop_table('athlete_stats')
    op.drop_table('users')
    op.drop_table('teams')
    op.drop_table('athletes')
