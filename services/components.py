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


async def get_components(session: AsyncSession) -> list[Component]:
    stmt = select(Component).order_by(Component.id)
    result_query = await session.execute(stmt)
    return list(result_query.scalars().all())


async def get_component(id: int, session: AsyncSession) -> Component:
    stmt = select(Component).where(Component.id == id)
    result_query = await session.execute(stmt)
    return result_query.scalar()

    # return await session.get(Component, id)


async def update_components(data: ComponentsSchemas, session: AsyncSession, id: int):
    component = await get_component(id, session)
    component.name = data.name
    component.quantity = data.quantity
    component.price = data.price

    session.add(component)
    await session.commit()
    # session.refresh(component)

    return component


async def remove_components(id: int, session: AsyncSession):
    component = await get_component(id, session)

    await session.delete(component)
    await session.commit()
