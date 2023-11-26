from fastapi import APIRouter, Depends
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
async def get(
    id: int = None,
    session: AsyncSession = Depends(db_helper.scope_session_dependebcy),
):
    return await semifinished.get(id, session)


@router.put("/", tags=["semifinished"])
async def update(
    data: SemifinishedSchemas = None, id: int = None, db: Session = Depends(get_db)
):
    return semifinished.update(data, id, db)


@router.delete("/", tags=["semifinished"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return semifinished.delete(id, db)
