from sqlalchemy import select, Result
from sqlalchemy.orm import Session, selectinload, load_only, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from models.product import Product
from models.semifinished import SemiFinished
from models.component import Component
from models.product_component import ProductComponent
from models.product_semifinished import ProductSemiFinished
from models.semifinished_component import SemiFinishedComponent
from models.product_product import ProductProduct
from schemas.product import ProductSchemas


async def create(data: ProductSchemas, session: AsyncSession):
    """Создает новый Товар и связь с полуфабрикатами и компонентами"""
    new_product = Product(
        name=data.name,
        quantity=data.quantity,
        price=data.price,
    )

    if data.component_list:
        for asoc_component in data.component_list:
            stmt = select(Component).where(Component.id == asoc_component.component_id)

            result_query = await session.execute(stmt)  # type: Result
            component = result_query.scalar()  # type: Component

            new_product.component_list.append(
                ProductComponent(
                    component=component,
                    component_count=asoc_component.count,
                )
            )

    if data.semifinished_list:
        for asoc_semifinished in data.semifinished_list:
            stmt = select(SemiFinished).where(
                SemiFinished.id == asoc_semifinished.semifinished_id
            )
            result_query = await session.execute(stmt)  # type: Result
            semifinished = result_query.scalar()  # type: SemiFinished

            new_product.semifinished_list.append(
                ProductSemiFinished(
                    semifinished=semifinished,
                    semifinished_count=asoc_semifinished.count,
                )
            )

    if data.product_list:
        for asoc_product in data.product_list:
            stmt = select(Product).where(Product.id == asoc_product.product_id)

            result_query = await session.execute(stmt)  # type: Result
            product = result_query.scalar()  # type: Product

            new_product.product_list.append(
                ProductProduct(
                    child_product=product,
                    child_product_id=product.id,
                    child_product_count=asoc_product.count,
                )
            )

    session.add(new_product)
    await session.commit()
    """ Та же проблема, не получаеться без рефреша вернуть объект, но после рефреша теряются все зависимости :/ """
    await session.refresh(new_product)

    return new_product


async def get_product(id: int, session: AsyncSession):
    """Возвращает товар и списки связанных полуфабрикатов и компонентов"""
    stmt = (
        select(Product)
        .where(Product.id == id)
        .options(
            selectinload(Product.component_list)
            .options(load_only(ProductComponent.component_count))
            .joinedload(ProductComponent.component)
        )
        .options(
            selectinload(Product.semifinished_list)
            .options(load_only(ProductSemiFinished.semifinished_count))
            .joinedload(ProductSemiFinished.semifinished)
        )
        .options(
            selectinload(Product.product_list)
            .options(load_only(ProductProduct.child_product_count))
            .joinedload(ProductProduct.child_product)
        )
    )
    result_query = await session.execute(stmt)
    return result_query.scalar()


async def get_products(session: AsyncSession):
    stmt = (
        select(Product)
        .options(
            selectinload(Product.component_list)
            .options(load_only(ProductComponent.component_count))
            .joinedload(ProductComponent.component)
        )
        .options(
            selectinload(Product.semifinished_list)
            .options(load_only(ProductSemiFinished.semifinished_count))
            .joinedload(ProductSemiFinished.semifinished)
        )
        .options(
            selectinload(Product.product_list)
            .options(load_only(ProductProduct.child_product_count))
            .joinedload(ProductProduct.child_product)
        )
    )
    result_query = await session.execute(stmt)
    return result_query.scalars().all()


async def get_with_semi_finished_components(id: int, session: AsyncSession):
    """Возвращает товар и списки связанных полуфабрикатов и компонентов
    и компоненты каждого полуфабриката"""
    stmt2 = (
        select(Product)
        .where(Product.id == id)
        .options(
            selectinload(Product.component_list)
            .options(load_only(ProductComponent.component_count))
            .joinedload(ProductComponent.component)
        )
        .options(
            selectinload(Product.semifinished_list)
            .options(load_only(ProductSemiFinished.semifinished_count))
            .joinedload(ProductSemiFinished.semifinished)
            .options(
                selectinload(SemiFinished.component_list)
                .options(load_only(SemiFinishedComponent.component_count))
                .joinedload(SemiFinishedComponent.component)
            )
        )
        .options(
            selectinload(Product.product_list)
            .options(load_only(ProductProduct.child_product_count))
            .joinedload(ProductProduct.child_product)
        )
    )
    result_query = await session.execute(stmt2)

    return list(result_query.scalars().all())


async def update(data: ProductSchemas, id: int, session: AsyncSession):
    """Обновляет информацию о товаре и связанных полуфабрикатах и компонентах"""
    product = await get_product(id, session)  # type: Product

    """ Если у товара были компоненту удаляем"""
    if product.component_list:
        for component in product.component_list:
            await session.delete(component)

    """ Если у товара были полуфабрикаты удаляем"""
    if product.semifinished_list:
        for semifinished in product.semifinished_list:
            await session.delete(semifinished)

    """ Если у товара были товары удаляем"""
    if product.product_list:
        for product in product.product_list:
            await session.delete(product)

    product = await create(data, session)

    return product


async def delete(id: int, session: AsyncSession):
    """Удаляет товар и все связи с полуфабрикатами и компонентами"""
    product = await get_product(id, session)  # type: Product

    if product:
        """Если у товара были компоненту удаляем"""
        if product.component_list:
            for component in product.component_list:
                await session.delete(component)

        """ Если у товара были полуфабрикаты удаляем"""
        if product.semifinished_list:
            for semifinished in product.semifinished_list:
                await session.delete(semifinished)

        """ Если у товара были товары удаляем"""
        if product.product_list:
            for product in product.product_list:
                await session.delete(product)

        await session.delete(product)
        await session.commit()
    else:
        return None


def get_component_count_by_prod(product: Product):
    """Возвращает словарь с компонентами или текст ошибки"""
    result_components = {}  # Результат - Dict[Компонент, int]

    def count_recursive(data, multiple: int = 1):
        """Функция рекурсивно подсчитывает количество всех компонентов входящих в товар"""
        if hasattr(data, "component_list"):
            for com_item in data.component_list:
                # com, count = dict.values()
                result_components[com_item.component_id] = (
                    result_components.get(com_item.component_id, 0)
                    + com_item.component_count * multiple
                )

        if hasattr(data, "semifinished_list"):
            for sem_item in data.semifinished_list:
                count_recursive(
                    sem_item.semifinished, sem_item.semifinished_count * multiple
                )

        # if "list_prod" in data:
        #     for prod_item in data["list_prod"]:
        #         count_recursive(prod_item["prod"], prod_item["count"] * multiple)

    count_recursive(product)

    return result_components


def get_product_with_all_component(id: int, session: AsyncSession):
    product = get_with_semi_finished_components(id, session)

    return get_component_count_by_prod(product)
