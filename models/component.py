from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped

from models.base import Base

if TYPE_CHECKING:
    from .semifinished_component import SemiFinishedComponent
    from .product_component import ProductComponent

# Компоненты
class Component(Base):
    name: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[int]

    # Связь на модель ассоциаций с полуфабрикатами
    semifinished_list: Mapped[list["SemiFinishedComponent"]] = relationship(back_populates="component")

    # Связь на модель ассоциаций с товарами
    product_list: Mapped[list["ProductComponent"]] = relationship(back_populates="component")

    # Сквозная связь с Полуфабрикатами
    # semifinisheds: Mapped[list["SemiFinished"]] = relationship(
    #     back_populates="components",
    #     secondary="semifinishedcomponent"
    # )