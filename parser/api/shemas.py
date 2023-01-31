from pydantic import BaseModel
from datetime import date

#########################
# BLOCK WITH API MODELS #
#########################


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowColor(TunedModel):
    id: int
    name: str


class ShowSize(TunedModel):
    id: int
    name: str
    amount: int


class ShowCategory(TunedModel):
    id: int
    name: str
    parent_id: int
    shard: str
    query: str
    url: str
    children: bool
    goods_displayed: bool


class ShowGoodsCatalogue(TunedModel):
    id: int
    name: str
    catalogue_id: int
    appeared: date


class ShowGoodsCards(TunedModel):
    id: int
    catalogue_id: int
    name: str
    brand: str
    brand_id: int
    sale: int
    price_full: int
    price_with_discount: int
    in_stock: int
    rating: int
    feedbacks: int
    # colors: ShowColor
    # sizes: ShowSize
