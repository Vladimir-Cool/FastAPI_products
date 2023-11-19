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
    # product_id_list: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=True)


    component_list: Mapped[list["ProductComponent"]] = relationship(back_populates="product",)
    semifinished_list: Mapped[list["ProductSemiFinished"]] = relationship(back_populates="product")

# ????
#     product_list: Mapped[list["ProductProduct"]] = relationship(backref=backref("parent_product"),
#                                                          foreign_keys="Product.product_id_list",
#                                                          remote_side="Product.id")


    # parent_product: Mapped["Product"] = relationship(back_populates="product_list")


