from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import Base

if TYPE_CHECKING:
    from .semifinished_component import SemiFinishedComponent
    from .product_semifinished import ProductSemiFinished


# Полуфабрикаты
class SemiFinished(Base):
    name: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[int]

    # Связь на таблицу ассоциаций
    component_list: Mapped[list["SemiFinishedComponent"]] = relationship(
        back_populates="semifinished"
    )
    product_list: Mapped[list["ProductSemiFinished"]] = relationship(
        back_populates="semifinished"
    )

    # Сквозная связь
    # components: Mapped[list["Component"]] = relationship(
    #     back_populates="semifinisheds",
    #     secondary="semifinishedcomponent"
    # )
