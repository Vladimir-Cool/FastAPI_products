from sqlalchemy import select, Result
from sqlalchemy.orm import Session, selectinload, load_only
from sqlalchemy.ext.asyncio import AsyncSession

from models import SemiFinished
from models.component import Component
from models.semifinished import SemiFinished
from models.semifinished_component import SemiFinishedComponent
from models.product_semifinished import ProductSemiFinished
from schemas.semifinished import SemifinishedSchemas


async def create_semifinished(
    data: SemifinishedSchemas,
    session: AsyncSession,
) -> SemiFinished:
    """Создаем полуфабрикат и связанные с ним компоненты
    Компоненты должны существовать иначе ошибка.
    Для параллельного создания и компонентов компонента нужно дописывать функции"""
    new_semifinished: SemiFinished = SemiFinished(
        name=data.name,
        quantity=data.quantity,
        price=data.price,
    )

    for asoc_component in data.components:
        stmt = select(Component).where(Component.id == asoc_component.component_id)
        result_query = await session.execute(stmt)
        component = result_query.scalar()

        new_semifinished.component_list.append(
            SemiFinishedComponent(
                component_count=asoc_component.count,
                component=component,
            )
        )

    session.add(new_semifinished)
    await session.commit()

    """ Рефреш нужен иначе 'jsonable_encoder' функция не может привести к json объект new_semifinihed.
        Вернется объект SemiFinished без связей, но связи создадуться"""
    await session.refresh(new_semifinished)
    print(new_semifinished)
    return new_semifinished


async def get_semifinished(id: int, session: AsyncSession) -> SemiFinished:
    """Возвращает полуфабрикат и компоненты из которого он состоит"""
    stmt = (
        select(SemiFinished)
        .where(SemiFinished.id == id)
        .options(
            selectinload(SemiFinished.component_list)
            .options(load_only(SemiFinishedComponent.component_count))
            .joinedload(SemiFinishedComponent.component)
        )
    )
    result_query = await session.execute(stmt)

    return result_query.scalar()


async def get_semifinisheds(session: AsyncSession):
    stmt = select(SemiFinished).options(
        selectinload(SemiFinished.component_list)
        .options(load_only(SemiFinishedComponent.component_count))
        .joinedload(SemiFinishedComponent.component)
    )
    result_query = await session.execute(stmt)

    return list(result_query.scalars().all())


async def update(
    data: SemifinishedSchemas,
    id: int,
    session: AsyncSession,
):
    """Изменяет Полуфабрикат и компоненты из которых он состояит
    Связи меняются:
        -удаляем все связи
        -создаем новые
    """
    # semifinished = await get_semifinished(id, session)        # type: SemiFinished

    stmt = (
        select(SemiFinished)
        .where(SemiFinished.id == id)
        .options(selectinload(SemiFinished.component_list))
    )

    result_query = await session.execute(stmt)  # type: Result

    semifinished = result_query.scalar()  # type: SemiFinished

    semifinished.name = data.name
    semifinished.quantity = data.quantity
    semifinished.price = data.price

    # Удаляем все связи если они есть
    if semifinished.component_list:
        for association in semifinished.component_list:
            await session.delete(association)

    # Добавляе новые связи
    """ Код дублируеться, надо выносить в отдельную функцию!!!"""
    for asoc_component in data.components:
        stmt = select(Component).where(Component.id == asoc_component.component_id)
        result_query = await session.execute(stmt)
        component = result_query.scalar()

        semifinished.component_list.append(
            SemiFinishedComponent(
                component_count=asoc_component.count,
                component=component,
            )
        )

    await session.commit()
    await session.refresh(semifinished)

    return semifinished


async def delete(id: int, session: AsyncSession):
    """Удаление полуфабриката по id"""
    stmt = (
        select(SemiFinished)
        .where(SemiFinished.id == id)
        .options(selectinload(SemiFinished.component_list))
        .options(selectinload(SemiFinished.product_list))
    )

    result_query = await session.execute(stmt)  # type: Result

    semifinished = result_query.scalar()  # type: SemiFinished

    # Если полуфабрикат есть
    if semifinished:
        # Удаляем все связи с компонентами
        if semifinished.component_list:
            for association in semifinished.component_list:
                await session.delete(association)
        # Удаляем все связи с товарами
        if semifinished.product_list:
            for associaciot in semifinished.product_list:
                await session.delete(associaciot)

        # Удаляем полуфабрикат
        await session.delete(semifinished)
        await session.commit()

    else:
        return None
