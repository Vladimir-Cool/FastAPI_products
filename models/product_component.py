from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import Base

if TYPE_CHECKING:
    from .product import Product
    from .component import Component

# Связь Товара - Компоненты
class ProductComponent(Base):
    __table_arg__ = (
        UniqueConstraint(
            "product_id",
            "component_id",
            name="Index_prod_com"
        )
    )

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    component_id: Mapped[int] = mapped_column(ForeignKey("component.id"))
    component_count: Mapped[int] = mapped_column(default=1, server_default="1")

    product: Mapped["Product"] = relationship(back_populates="component_list")
    component: Mapped["Component"] = relationship(back_populates="product_list")