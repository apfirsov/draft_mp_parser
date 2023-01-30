from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from db.dals import ParserDAL
# from db.models import ParserItem
from db.session import get_db
from db.dals import GoodsCardsDLA, GoodsCatalogueDLA, CategoryDLA
from db.models import GoodsCards, GoodsCatalogue, Category

#########################
# BLOCK WITH API ROUTES #
#########################

parser_router = APIRouter()


async def _get_all(user_id, db) -> Union[ShowUser, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(
                user_id=user_id,
            )
            if user is not None:
                return ShowUser(
                    user_id=user.user_id,
                    name=user.name,
                    surname=user.surname,
                    email=user.email,
                    is_active=user.is_active,
                )


@parser_router.get("/goods_cards")
async def get_goods_cards(
    db: AsyncSession = Depends(get_db)
) -> List[GoodsCards]:
    async with db as session:
        async with session.begin():
            parser_dal = GoodsCardsDLA(session)
            return await parser_dal.get_all_items()


@parser_router.get("/goods_catalogue")
async def get_goods_catalogue(
    db: AsyncSession = Depends(get_db)
) -> List[GoodsCatalogue]:
    async with db as session:
        async with session.begin():
            parser_dal = GoodsCatalogueDLA(session)
            return await parser_dal.get_all_items()


@parser_router.get("/category")
async def get_category(
    db: AsyncSession = Depends(get_db)
) -> List[Category]:
    async with db as session:
        async with session.begin():
            parser_dal = CategoryDLA(session)
            return await parser_dal.get_all_items()
