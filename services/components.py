from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.components import ComponentsSchemas
from models.component import Component


async def create_components(data: ComponentsSchemas, session: AsyncSession):
    new_component = Component(
        name=data.name,
        quantity=data.quantity,
        price=data.price,
    )

    session.add(new_component)
    await session.commit()
    # await session.refresh(new_component)
    return new_component


async def get_component(id: int, session: AsyncSession):
    return await session.get(Component, id)


def update_components(data: ComponentsSchemas, db: Session, id: int):
    try:
        component = db.query(Component).filter(Component.id == id).first()
        component.name = data.name
        component.quantity = data.quantity
        component.price = data.price

        db.add(component)
        db.commit()
        db.refresh(component)
    except Exception as e:
        component = []
        print(e)

    return component


def remove_components(id: int, db: Session):
    component = db.query(Component).filter(Component.id == id).delete()
    try:
        db.commit()
    except Exception as e:
        print(e)

    return component
