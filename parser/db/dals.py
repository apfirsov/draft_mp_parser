from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ParserItem

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class ParserDAL:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_items(self) -> List[ParserItem]:
        query = await self.db_session.execute(
            select(ParserItem).order_by(ParserItem.prod_id)
        )
        return query.scalars().all()
