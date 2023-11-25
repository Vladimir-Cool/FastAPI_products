from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref

from models.base import Base

if TYPE_CHECKING:
    from .product_component import ProductComponent
    from .product_semifinished import ProductSemiFinished
    from .product_product import ProductProduct


# Товары
class Product(Base):
    name: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[int]
    # parent_product: Mapped[int] = mapped_column(nullable=True)

    component_list: Mapped[list["ProductComponent"]] = relationship(
        back_populates="product",
    )
    semifinished_list: Mapped[list["ProductSemiFinished"]] = relationship(
        back_populates="product"
    )

    # Сквозная связь самого на себя работает, но как достать count из таблицы асоцциаций???
    parent_product: Mapped["Product"] = relationship(
        "Product",
        secondary="productproduct",
        primaryjoin="Product.id==ProductProduct.child_product_id",
        secondaryjoin="Product.id==ProductProduct.parent_product_id",
        back_populates="product_list",
    )
    product_list: Mapped[list["Product"]] = relationship(
        "Product",
        secondary="productproduct",
        primaryjoin="Product.id==ProductProduct.parent_product_id",
        secondaryjoin="Product.id==ProductProduct.child_product_id",
        back_populates="parent_product",
    )

    # childe_product_list: Mapped[list["ProductProduct"]] = relationship(
    #     "ProductProduct",
    #     back_populates="parent_product",
    #     foreign_keys="ProductProduct.parent_product_id",
    # )


# parent_product: Mapped["Product"] = relationship(back_populates="product_list")
