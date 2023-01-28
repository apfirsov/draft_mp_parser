from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals import ParserDAL
from db.models import ParserItem
from db.session import get_db

#########################
# BLOCK WITH API ROUTES #
#########################

parser_router = APIRouter()

@parser_router.get("/all")
async def get_parsers(db: AsyncSession = Depends(get_db)) -> List[ParserItem]:
    async with db as session:
        async with session.begin():
            parser_dal = ParserDAL(session)
            return await parser_dal.get_all_items()
