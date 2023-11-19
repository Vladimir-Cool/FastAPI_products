from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.bdconnect import get_db

from services import semifinished
from schemas.semifinished import SemifinishedSchemas

router = APIRouter()

@router.post("/", tags=["semifinished"])
async def create(data: SemifinishedSchemas = None, db: Session = Depends(get_db)):
    return semifinished.create(data, db)

@router.get("/", tags=["semifinished"])
async def get(id: int = None, db: Session = Depends(get_db)):
    return semifinished.get(id, db)

@router.put("/", tags=["semifinished"])
async def update(data: SemifinishedSchemas = None, id: int = None,  db: Session = Depends(get_db)):
    return semifinished.update(data, id, db)

@router.delete("/", tags=["semifinished"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return semifinished.delete(id, db)

