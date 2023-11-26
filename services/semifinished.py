from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload, load_only
from sqlalchemy.ext.asyncio import AsyncSession

from models.component import Component
from models.semifinished import SemiFinished
from models.semifinished_component import SemiFinishedComponent
from schemas.semifinished import SemifinishedSchemas


async def create_semifinished(
    data: SemifinishedSchemas,
    session: AsyncSession,
) -> SemiFinished:
    """Создаем полуфабрикат и связанные с ним компоненты
    Компоненты должны существовать иначе ошибка.
    Для параллельного создания и компонентов компонента нужно дописывать функции"""
    new_semifinished = SemiFinished(
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
    # await.session.refresh(new_semifinished)

    return new_semifinished


async def get(id: int, session: AsyncSession):
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


def update(data: SemifinishedSchemas, id: int, db: Session):
    """Изменяет Полуфабрикат и компоненты из которых он состояит
    Связи меняются:
        -удаляем все связи
        -создаем новые
    """
    semifinished = get(id, db)  # type: SemiFinished

    semifinished.name = data.name
    semifinished.quantity = data.quantity
    semifinished.price = data.price

    # Удаляем все связи
    for association in semifinished.component_list:
        db.delete(association)

    # Добавляе новые связи
    """ Код дублируеться, надо выносить в отдельную функцию!!!"""
    for asoc_component in data.components:
        stmt = select(Component).where(Component.id == asoc_component.component)

        component = db.execute(stmt).scalar()

        semifinished.component_list.append(
            SemiFinishedComponent(
                component_count=asoc_component.count, component=component
            )
        )

    db.commit()
    db.refresh(semifinished)

    return semifinished


def delete(id: int, db: Session):
    """Удаление полуфабриката по id"""
    semifinished = get(id, db)  # type: SemiFinished

    # Удаляем все связи
    if semifinished.component_list:
        for component in semifinished.component_list:
            db.delete(component)
        db.commit()

    # Удаляем полуфабрикат
    db.delete(semifinished)
    db.commit()

    return semifinished
