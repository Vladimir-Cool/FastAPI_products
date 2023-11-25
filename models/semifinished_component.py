from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import Base

if TYPE_CHECKING:
    from .semifinished import SemiFinished
    from .component import Component


# Связь Полуфабрикаты - Компоненты
class SemiFinishedComponent(Base):
    __table_arg__ = UniqueConstraint(
        "semifinished_id", "component_id", name="Index_sem_com"
    )

    semifinished_id: Mapped[int] = mapped_column(ForeignKey("semifinished.id"))
    component_id: Mapped[int] = mapped_column(ForeignKey("component.id"))
    component_count: Mapped[int] = mapped_column(default=1, server_default="1")

    component: Mapped["Component"] = relationship(back_populates="semifinished_list")
    semifinished: Mapped["SemiFinished"] = relationship(back_populates="component_list")
