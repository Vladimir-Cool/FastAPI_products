from sqlalchemy.orm import Session, selectinload, load_only, joinedload
from sqlalchemy import select

from models.product import Product
from models.semifinished import SemiFinished
from models.component import Component
from models.product_component import ProductComponent
from models.product_semifinished import ProductSemiFinished
from models.semifinished_component import SemiFinishedComponent
from models.product_product import ProductProduct
from schemas.product import ProductSchemas


def create(data: ProductSchemas, db: Session):
    """Создает новый Товар и связь с полуфабрикатами и компонентами"""

    new_product = Product(name=data.name, quantity=data.quantity, price=data.price)

    if data.components:
        for asoc_component in data.components:
            stmt = select(Component).where(Component.id == asoc_component.component_id)

            component = db.execute(stmt).scalar()  # type: Component

            new_product.component_list.append(
                ProductComponent(
                    component=component,
                    component_count=asoc_component.count,
                )
            )

    if data.semifinisheds:
        for asoc_semifinished in data.semifinisheds:
            stmt = select(SemiFinished).where(
                SemiFinished.id == asoc_semifinished.semifinished_id
            )

            semifinished = db.execute(stmt).scalar()  # type: SemiFinished

            new_product.semifinished_list.append(
                ProductSemiFinished(
                    semifinished=semifinished,
                    semifinished_count=asoc_semifinished.count,
                )
            )

    if data.products:
        for asoc_product in data.products:
            stmt = select(Product).where(Product.id == asoc_product.product_id)

            product = db.execute(stmt).scalar()  # type: Product

            new_product.product_list.append(
                ProductProduct(
                    child_product=product,
                    child_product_id=product.id,
                    child_product_count=asoc_product.count,
                )
            )
    print(new_product.product_list)
    print("Commit")
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def get(id: int, db: Session):
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
        # .options(selectinload(Product.product_list))
        .options(
            selectinload(Product.product_list)
            .options(load_only(ProductProduct.child_product_count))
            .joinedload(ProductProduct.child_product)
        )
    )

    return db.execute(stmt).scalar()


def get_with_semi_finished_components(id: int, db: Session):
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

    return db.execute(stmt2).scalars().all()


def update(data: ProductSchemas, id: int, db: Session):
    """Обновляет информацию о товаре и связанных полуфабрикатах и компонентах"""
    product = get(id, db)  # type: Product

    """ Если у товара были компоненту удаляем"""
    if product.component_list:
        for component in product.component_list:
            db.delete(component)

    """ Код дублируется, надо вынести в отдельную функцию!!!"""
    if data.components:
        for asoc_component in data.components:
            stmt = select(Component).where(Component.id == asoc_component.component_id)

            component = db.execute(stmt).scalar()  # type: Component

            product.component_list.append(
                ProductComponent(
                    component=component, component_count=asoc_component.count
                )
            )

    """ Если у товара были полуфабрикаты удоляем"""
    if product.semifinished_list:
        for semifinished in product.semifinished_list:
            db.delete(semifinished)

    """ Код дублируется, надо вынести в отдельную функцию!!!"""
    if data.semifinisheds:
        for asoc_semifinished in data.semifinisheds:
            stmt = select(SemiFinished).where(
                SemiFinished.id == asoc_semifinished.semifinished_id
            )

            semifinished = db.execute(stmt).scalar()  # type: SemiFinished

            product.semifinished_list.append(
                ProductSemiFinished(
                    semifinished=semifinished,
                    semifinished_count=asoc_semifinished.count,
                )
            )

    db.commit()
    db.refresh(product)

    return product


def delete(id: int, db: Session):
    """Удаляет товар и все связи с полуфабрикатами и компонентами"""
    product = get(id, db)  # type: Product

    """ Если у товара были компоненту удаляем"""
    if product.component_list:
        for component in product.component_list:
            db.delete(component)
        db.commit()

    if product.semifinished_list:
        for semifinished in product.semifinished_list:
            db.delete(semifinished)
        db.commit()

    db.delete(product)
    db.commit()

    return product


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


def get_product_with_all_component(id: int, db: Session):
    product = get_with_semi_finished_components(id, db)

    return get_component_count_by_prod(product)
