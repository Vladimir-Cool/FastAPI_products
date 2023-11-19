# from typing import TYPE_CHECKING
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, backref

from models.base import Base

if TYPE_CHECKING:
    from .product import Product


# Связь Товары - Товар
class ProductProduct(Base):
    __table_arg__ = (
        UniqueConstraint(
            "child_product_id",
            "parent_product_id",
            name="Index_prod_prod"
        )
    )

    parent_product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    child_product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    child_product_count: Mapped[int]

    parent_product: Mapped["Product"] = relationship(backref=backref("product_list"), foreign_keys="ProductProduct.parent_product_id")
    child_product: Mapped["Product"] = relationship(foreign_keys="ProductProduct.child_product_id")


