from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Table
)
from sqlalchemy.orm import declarative_base, relationship

##############################
# BLOCK WITH DATABASE MODELS #
##############################


Base = declarative_base()


cards_color = Table(
    "cards_color",
    Base.metadata,
    Column("color_id", ForeignKey("Color.id"), primary_key=True),
    Column("goods_id", ForeignKey("Goods_Cards.id"), primary_key=True),
)


cards_size = Table(
    "cards_size",
    Base.metadata,
    Column("size_id", ForeignKey("Size.id"), primary_key=True),
    Column("goods_id", ForeignKey("Goods_Cards.id"), primary_key=True),
    Column("size_amount", Integer),
)


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
        "Color",
        secondary=cards_color,
        # back_populates="colors",
        cascade="all, delete"
    )
    sizes = relationship(
        "Size",
        secondary=cards_size,
        # back_populates="sizes",
        cascade="all, delete"
    )


class Color(Base):
    __tablename__ = "Color"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    cards_id = Column("card_id", Integer, ForeignKey('Goods_Cards.id'))


class Size(Base):
    __tablename__ = "Size"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    # amount = Column("amount", Integer)
    cards_id = Column("card_id", Integer, ForeignKey('Goods_Cards.id'))
