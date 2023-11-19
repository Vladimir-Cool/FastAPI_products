from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.bdconnect import get_db

from services import product
from schemas.product import ProductSchemas

router = APIRouter()

@router.post("/", tags=["product"])
async def create(data: ProductSchemas = None, db: Session = Depends(get_db)):
    return product.create(data, db)


@router.get("/", tags=["product"])
async def get(id: int = None, db: Session = Depends(get_db)):
    """ Вернет продукт и его компоненты и полуфабрикаты"""
    return product.get(id, db)


@router.get("/sem_comp", tags=["product"])
async def get_with_semi_finished_components(id: int = None, db: Session = Depends(get_db)):
    """ Вернет продукт и его компоненты и полуфабрикаты
        + компоненты полуфабрикатов"""
    return product.get_with_semi_finished_components(id, db)


@router.get("/com", tags=["product"])
async def get_product_all_component(id: int = None, db: Session = Depends(get_db)):
    """ Пока что возвразает id, count всех компонентов Товара"""
    return product.get_product_with_all_component(id, db)


@router.put("/", tags=["product"])
async def update(data: ProductSchemas = None, id: int = None, db: Session = Depends(get_db)):
    return product.update(data, id, db)


@router.delete("/", tags=["product"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return product.delete(id, db)

