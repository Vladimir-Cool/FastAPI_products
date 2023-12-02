from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from utils.bdconnect import get_db, db_helper

from services import semifinished
from schemas.semifinished import SemifinishedSchemas

router = APIRouter()


@router.post("/", tags=["semifinished"])
async def create(
    data: SemifinishedSchemas = None,
    session: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    return await semifinished.create_semifinished(data, session)


@router.get("/", tags=["semifinished"])
async def gets(
    session: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    return await semifinished.get_semifinisheds(session)


@router.get("/{id}", tags=["semifinished"])
async def get(
    id: int = None,
    session: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    return await semifinished.get_semifinished(id, session)


@router.put("/{id}", tags=["semifinished"])
async def update(
    data: SemifinishedSchemas = None,
    id: int = None,
    session: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    return await semifinished.update(data, id, session)


@router.delete("/{id}", tags=["semifinished"], status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: int = None, session: AsyncSession = Depends(db_helper.scope_session_dependebcy)
):
    return await semifinished.delete(id, session)
