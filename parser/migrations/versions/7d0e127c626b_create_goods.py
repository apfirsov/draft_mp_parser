"""create_goods

Revision ID: 7d0e127c626b
Revises: 768df11d5228
Create Date: 2023-01-31 01:12:30.935302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d0e127c626b'
down_revision = '768df11d5228'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Goods_Cards_catalogue_id_fkey', 'Goods_Cards', type_='foreignkey')
    op.drop_column('Goods_Cards', 'catalogue_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Goods_Cards', sa.Column('catalogue_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('Goods_Cards_catalogue_id_fkey', 'Goods_Cards', 'Goods_Catalogue', ['catalogue_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
