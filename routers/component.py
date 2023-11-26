from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


from utils.bdconnect import get_db, db_helper
from services import component
from schemas.components import ComponentsSchemas

router = APIRouter()


@router.post("/", tags=["components"])
async def create(
    data: ComponentsSchemas = None,
    session: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    return await component.create_components(data, session)


@router.get("/", tags=["components"])
async def gets(session: AsyncSession = Depends(db_helper.scope_session_dependebcy)):
    return await component.get_components(session)


@router.get("/{id}", tags=["components"])
async def get(
    id: int = None,
    session: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    return await component.get_component(id, session)


@router.put("/{id}", tags=["components"])
async def update(
    data: ComponentsSchemas = None,
    session: AsyncSession = Depends(db_helper.scope_session_dependebcy),
    id: int = None,
):
    return await component.update_components(data, session, id)


@router.delete("/{id}", tags=["components"], status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: int = None,
    session: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    return await component.remove_components(id, session)
