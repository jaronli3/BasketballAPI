"""create team_predictions table

Revision ID: 4c15ee86918d
Revises: 
Create Date: 2023-05-16 14:23:22.006404

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4c15ee86918d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

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
        'athletes',
        sa.Column('athlete_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.Text, nullable=False)
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
        'teams',
        sa.Column('team_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('team_abbrev', sa.Text, nullable=False),
        sa.Column('team_name', sa.Text, nullable=False)
    )

    op.create_table(
        'team_ratings',
        sa.Column('team_rating_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('team_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['team_id'], ['teams.team_id']),
        sa.Column('rating', sa.Integer, nullable=False)
    )

    op.create_table(
        'athlete_ratings',
        sa.Column('athlete_rating_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('athlete_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(['athlete_id'], ['athletes.athlete_id']),
        sa.Column('rating', sa.Integer, nullable=False)
    )


def downgrade() -> None:

    op.drop_table('athlete_stats')
    op.drop_table('athletes')
    op.drop_table('games')
    op.drop_table('teams')
    op.drop_table('team_ratings')
    op.drop_table('athlete_ratings')