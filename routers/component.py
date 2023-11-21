from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


from utils.bdconnect import get_db, db_helper
from services import components
from schemas.components import ComponentsSchemas

router = APIRouter()


@router.post("/", tags=["components"])
async def create(
    data: ComponentsSchemas = None,
    db: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    return await components.create_components(data, db)


@router.get("/{id}", tags=["components"])
async def get(
    id: int = None,
    db: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    return await components.get_component(id, db)


@router.put("/{id}", tags=["components"])
async def update(
    data: ComponentsSchemas = None,
    db: Session = Depends(get_db),
    id: int = None,
):
    return components.update_components(data, db, id)


@router.delete("/{id}", tags=["components"])
async def delete(
    id: int = None,
    db: Session = Depends(get_db),
):
    return components.remove_components(id, db)
