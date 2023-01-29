from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Table
)
from sqlalchemy.orm import declarative_base, relationship, backref

##############################
# BLOCK WITH DATABASE MODELS #
##############################


Base = declarative_base()


class Card_Colors(Base):
    __tablename__ = 'cards_color'
    id = Column(Integer, primary_key=True, unique=True)
    color_id = Column(
        "color_id",
        Integer,
        ForeignKey(
            "Colors.id"
        ),
        primary_key=True
    )
    card_id = Column(
        "card_id",
        Integer,
        ForeignKey(
            "Goods_Cards.id"
        ),
        primary_key=True
    )
    color = relationship(
        "Colors",
        backref=backref(
            "cards_color",
            cascade="all, delete-orphan"
        )
    )
    card = relationship(
        "GoodsCards",
        backref=backref(
            "cards_color",
            cascade="all, delete-orphan"
        )
    )


class Colors(Base):
    __tablename__ = "Colors"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)


class Category(Base):
    __tablename__ = "Category"

    id = Column(
        "id",
        Integer,
        primary_key=True
    )
    name = Column(
        "name",
        String,
    )
    parent_id = Column(
        "parent_id",
        Integer
    )  # возможно значениее поумолчанию
    shard = Column(
        "category_shard",
        String
    )
    query = Column(
        "query",
        String
    )
    url = Column(
        "url",
        String
    )
    children = Column(
        "children",
        Boolean
    )
    goods_displayed = Column(
        "displayed",
        Boolean
    )


class GoodsCatalogue(Base):
    __tablename__ = "Goods_Catalogue"

    id = Column(
        "id",
        Integer,
        primary_key=True
    )
    name = Column(
        "name",
        String
    )
    catalogue_id = Column(
        "catalogue_id",
        Integer,
        ForeignKey(
            "Category.id",
            ondelete="CASCADE"
        )
    )
    appeared = Column(
        "appeared",
        DateTime
    )


class GoodsCards(Base):
    __tablename__ = "Goods_Cards"

    id = Column(
        "id",
        Integer,
        primary_key=True
    )
    catalogue_id = Column(
        "catalogue_id",
        Integer,
        ForeignKey(
            "Goods_Catalogue.id",
            ondelete="CASCADE"
        )
    )
    name = Column(
        "name",
        String
    )
    brand = Column(
        "brand",
        String
    )
    brand_id = Column(
        "brand_id",
        Integer
    )
    sale = Column(
        "sale",
        Integer
    )
    price_full = Column(
        "price_full",
        Integer
    )
    price_with_discount = Column(
        "price_with_discount",
        Integer
    )
    in_stock = Column(
        "in_stock",
        Integer
    )
    rating = Column(
        "rating",
        Integer
    )
    feedbacks = Column(
        "feedbacks",
        Integer
    )
    colors = relationship(
        "Colors",
        secondary="cards_color"
    )
    # sizes = relationship(
    #     "Sizes",
    #     secondary=cards_size,
    #     backref='Goods_Cards'
    # )
