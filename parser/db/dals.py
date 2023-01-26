from typing import List, Union, Optional

from sqlalchemy import select, update
# from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Parser

###########################################################
# BLOCK FOR INTERACTION WITH DATABASE IN BUSINESS CONTEXT #
###########################################################


class ParserDAL:
    """Data Access Layer for operating user info"""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_parser(
        self,
        prod_id: int,
        name: str,
        category: str,
        price: int,
        rest_goods: int,
        link: str,
        seller: str,
    ) -> Parser:
        new_parser = Parser(
            prod_id=prod_id,
            name=name,
            category=category,
            price=price,
            rest_goods=rest_goods,
            link=link,
            seller=seller,
        )
        self.db_session.add(new_parser)
        await self.db_session.flush()
        return new_parser

    async def get_parser_for_id(self, prod_id: int) -> Union[Parser, None]:
        query = select(Parser).where(Parser.prod_id == prod_id)
        res = await self.db_session.execute(query)
        parser_row = res.fetchone()
        if parser_row is not None:
            return parser_row[0]

    async def get_parsers(self) -> List[Parser]:
        query = await self.db_session.execute(
            select(Parser).order_by(Parser.prod_id)
        )
        return query.scalars().all()
