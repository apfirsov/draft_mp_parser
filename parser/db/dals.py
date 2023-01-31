from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from db.models import ParserItem
from db.models import (
    Category,
    GoodsCatalogue,
    GoodsCards,
    Color
)

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class ColorsDLA:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession, card_id):
        self.db_session = db_session
        self.card_id = card_id

    async def get_color(self) -> List[Color]:
        query = await self.db_session.execute(
            select(Color).filter(card_id=self.card_id)
        )
        return query.scalars().all()


class GoodsCardsDLA:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_items(self) -> List[GoodsCards]:
        query = await self.db_session.execute(
            select(GoodsCards, Category).order_by(GoodsCards.id)
        )
        return query.scalars().all()


class GoodsCatalogueDLA:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_items(self) -> List[GoodsCatalogue]:
        query = await self.db_session.execute(
            select(GoodsCatalogue).order_by(GoodsCatalogue.id)
        )
        return query.scalars().all()


class CategoryDLA:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_items(self) -> List[Category]:
        query = await self.db_session.execute(
            select(Category).order_by(Category.id)
        )
        return query.scalars().all()
