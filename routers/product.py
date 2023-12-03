from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from utils.bdconnect import db_helper

from services import product
from schemas.product import ProductSchemas

router = APIRouter()


@router.post("/", tags=["product"])
async def create(
    data: ProductSchemas = None,
    session: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    """Создаем новый продукт с указанием списков компонентов, полуфабрикатов и других товаров"""
    return await product.create(data, session)


@router.get("/", tags=["product"])
async def gets(session: AsyncSession = Depends(db_helper.scope_session_dependebcy)):
    """Возвращает все товары со списками компонентов, полуфабрикатов и других товаров"""
    return await product.get_products(session)


@router.get("/{id}", tags=["product"])
async def get(
    id: int = None,
    session: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    """Возвращает товар по ID вместе со списками компонентов, полуфабрикатов и других товаров"""
    return await product.get_product(id, session)


@router.get("/sem_comp/{id}", tags=["product"])
async def get_with_semi_finished_components(
    id: int = None, session: AsyncSession = Depends(db_helper.scope_session_dependebcy)
):
    """Вернет продукт и его компоненты и полуфабрикаты и компоненты полуфабрикатов"""
    return await product.get_with_semi_finished_components(id, session)


@router.get("/com/{id}", tags=["product"])
async def get_product_all_component(
    id: int = None, session: AsyncSession = Depends(db_helper.scope_session_dependebcy)
):
    """Возвращает список всех"""
    return await product.get_product_with_all_component(id, session)


@router.put("/{id}", tags=["product"])
async def update(
    data: ProductSchemas = None,
    id: int = None,
    session: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    return await product.update(data, id, session)


@router.delete("/{id}", tags=["product"], status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: int = None, session: AsyncSession = Depends(db_helper.scope_session_dependebcy)
):
    return await product.delete(id, session)
