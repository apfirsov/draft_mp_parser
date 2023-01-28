from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

##############################
# BLOCK WITH DATABASE MODELS #
##############################


Base = declarative_base()

# Изменить имя и содержание в зависимости от архитектуры
class ParserItem(Base):
    __tablename__ = "parser"

    prod_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Integer, nullable=True)
    rest_goods = Column(Integer, nullable=True)
    link = Column(String, nullable=False)
    seller = Column(String, nullable=False)
