from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

# from db.dals import ParserDAL
# from db.models import ParserItem
from db.session import get_db
from db.dals import GoodsCardsDLA, GoodsCatalogueDLA, CategoryDLA, ColorsDLA
from db.models import GoodsCards, GoodsCatalogue, Category
from api.shemas import ShowGoodsCards, ShowColor

#########################
# BLOCK WITH API ROUTES #
#########################

parser_router = APIRouter()


async def _get_all(db) -> List[ShowGoodsCards]:
    cards_list = []
    async with db as session:
        async with session.begin():
            cards_dal = GoodsCardsDLA(session)
            cards_all = await cards_dal.get_all_items()
            if cards_all is not None:
                for cards in cards_all:
                    cards_list.append(ShowGoodsCards(
                            id=cards.id,
                            catalogue_id=cards.catalogue_id,
                            name=cards.name,
                            brand=cards.brand,
                            brand_id=cards.brand_id,
                            sale=cards.sale,
                            price_full=cards.price_full,
                            price_with_discount=cards.price_with_discount,
                            in_stock=cards.in_stock,
                            rating=cards.rating,
                            feedbacks=cards.feedbacks,
                            colors=_get_color(db, card_id=id),
                            # sizes=cards.sizes
                        )
                    )
            return cards_list


async def _get_color(db, card_id) -> List[ShowColor]:
    color_list = []
    async with db as session:
        async with session.begin():
            color_dal = ColorsDLA(session)
            color_all = await color_dal.get_all_items(card_id)
            if color_all is not None:
                for cards in color_all:
                    color_list.append(ShowGoodsCards(
                            id=cards.id,
                            name=cards.name,
                            card_id=cards.card_id
                        )
                    )
            return color_list


@parser_router.get("/all")
async def get_all(db: AsyncSession = Depends(get_db)) -> List[ShowGoodsCards]:
    user = await _get_all(db)
    if user is None:
        raise HTTPException(
            status_code=404, detail="Not found."
        )
    return user

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
