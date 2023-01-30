from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from db.models import ParserItem
from db.models import (
    Category,
    GoodsCatalogue,
    GoodsCards
)

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


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
