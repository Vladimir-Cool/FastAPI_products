from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import Base

if TYPE_CHECKING:
    from .product import Product
    from .semifinished import SemiFinished

# Связь Товары - Полуфабрикаты
class ProductSemiFinished(Base):
    __table_arg__ = (
        UniqueConstraint(
            "product_id",
            "semifinished_id",
            name="Index_prod_com"
        )
    )

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    semifinished_id: Mapped[int] = mapped_column(ForeignKey("semifinished.id"))
    semifinished_count: Mapped[int] = mapped_column(default=1, server_default="1")

    product: Mapped["Product"] = relationship(back_populates="semifinished_list")
    semifinished: Mapped["SemiFinished"] = relationship(back_populates="product_list")
