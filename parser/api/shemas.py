from pydantic import BaseModel

#########################
# BLOCK WITH API MODELS #
#########################


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


# Изменить имя в зависимоти от архитектуры
class ShowItem(TunedModel):
    prod_id: int
    name: str
    category: str
    price: int
    rest_goods: int
    link: str
    seller: str
