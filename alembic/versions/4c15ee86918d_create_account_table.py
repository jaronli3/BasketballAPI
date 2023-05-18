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

prefix = "/Users/zach/Desktop/CSC_365/Project/"


def upgrade() -> None:

    op.create_table(
        'athletes',
        sa.Column('athlete_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.Text, nullable=False)
    )

    op.create_table(
        'teams',
        sa.Column('team_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('team_abbrev', sa.Text, nullable=False),
        sa.Column('team_name', sa.Text, nullable=False)
    )

    op.create_table(
        'athlete_stats',
        sa.Column('athlete_id', sa.Integer, primary_key=True),
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

    op.create_table(
        'games',
        sa.Column('game_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('home', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['home'], ['teams.team_id']),
        sa.Column('away', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['away'], ['teams.team_id']),
        sa.Column('winner', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['winner'], ['teams.team_id']),
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

    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.Text, nullable=False),
        sa.Column('hashed_password', sa.Text, nullable=False)
    )

    op.create_table(
        'team_ratings',
        sa.Column('team_rating_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('team_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['team_id'], ['teams.team_id']),
        sa.Column('rating', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'])
    )

    op.create_table(
        'athlete_ratings',
        sa.Column('athlete_rating_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('athlete_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['athlete_id'], ['athletes.athlete_id']),
        sa.Column('rating', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'])
    )

    # Ad hoc tables for insertion

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

    athletes = table(
        "athletes",
        Column("athlete_id", Integer),
        Column("name", Text)
    )

    games = table(
        "games",
        Column("game_id", Integer),
        Column("home", Integer),
        Column("away", Integer),
        Column("winner", Integer),
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

    teams = table(
        "teams",
        Column("team_id", Integer),
        Column("team_abbrev", Text),
        Column("team_name", Text)
    )

    with open(prefix + "data/athletes.csv", mode="r", encoding="utf-8") as csv_file:
        op.bulk_insert(athletes, [row for row in csv.DictReader(csv_file, skipinitialspace=True)])

    with open(prefix + "data/teams.csv", mode="r", encoding="utf-8") as csv_file:
        op.bulk_insert(teams, [row for row in csv.DictReader(csv_file, skipinitialspace=True)])

    with open(prefix + "data/athlete_stats.csv", mode="r", encoding="utf-8") as csv_file:
        op.bulk_insert(athlete_stats, [row for row in csv.DictReader(csv_file, skipinitialspace=True)])

    with open(prefix + "data/games.csv", mode="r", encoding="utf-8") as csv_file:
        op.bulk_insert(games, [row for row in csv.DictReader(csv_file, skipinitialspace=True)])




def downgrade() -> None:

    op.drop_table('athlete_ratings')
    op.drop_table('team_ratings')
    op.drop_table('games')
    op.drop_table('athlete_stats')
    op.drop_table('users')
    op.drop_table('teams')
    op.drop_table('athletes')




