"""create table for parser

Revision ID: 44298bcfaaeb
Revises: 
Create Date: 2023-01-24 22:43:11.239686

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '44298bcfaaeb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parser',
    sa.Column('prod_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('rest_goods', sa.Integer(), nullable=True),
    sa.Column('link', sa.String(), nullable=False),
    sa.Column('seller', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('prod_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parser')
    # ### end Alembic commands ###
