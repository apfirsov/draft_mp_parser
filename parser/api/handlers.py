from typing import List, Union, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import ParserCreate, ShowParser
from db.dals import ParserDAL
from db.models import Parser
from db.session import get_db

#########################
# BLOCK WITH API ROUTES #
#########################

parser_router = APIRouter()


async def _create_new_parse(body: ParserCreate, db) -> ShowParser:
    async with db() as session:
        async with session.begin():
            parser_dal = ParserDAL(session)
            parser = await parser_dal.create_parser(
                prod_id=body.prod_id,
                name=body.name,
                category=body.category,
                price=body.price,
                rest_goods=body.rest_goods,
                link=body.link,
                seller=body.seller,
            )
            return ShowParser(
                prod_id=parser.prod_id,
                name=parser.name,
                category=parser.category,
                price=parser.price,
                rest_goods=parser.rest_goods,
                link=parser.link,
                seller=parser.seller,
            )


async def _get_parser_for_id(prod_id, db) -> Union[ShowParser, None]:
    async with db as session:
        async with session.begin():
            parser_dal = ParserDAL(session)
            parser = await parser_dal.get_parser_for_id(
                prod_id=prod_id,
            )
            if parser is not None:
                return ShowParser(
                    prod_id=parser.prod_id,
                    name=parser.name,
                    category=parser.category,
                    price=parser.price,
                    rest_goods=parser.rest_goods,
                    link=parser.link,
                    seller=parser.seller,
                )


@parser_router.post("/", response_model=ShowParser)
async def create_parser(body: ParserCreate) -> ShowParser:
    return await _create_new_parse(body)


@parser_router.get("/", response_model=ShowParser)
async def get_parser_for_id(
    prod_id: int,
    db: AsyncSession = Depends(get_db)
) -> ShowParser:
    parser = await _get_parser_for_id(prod_id, db)
    if parser is None:
        raise HTTPException(
            status_code=404, detail=f"Parsers with id {prod_id} not found."
        )
    return parser


@parser_router.get("/all")
async def get_parsers(db: AsyncSession = Depends(get_db)) -> List[Parser]:
    async with db as session:
        async with session.begin():
            parser_dal = ParserDAL(session)
            return await parser_dal.get_parsers()
