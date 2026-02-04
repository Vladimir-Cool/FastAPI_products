from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field

from routers import component
from routers import semifinished
from routers import product


app = FastAPI(redoc_url=None)
app.include_router(component.router, prefix="/comp")
app.include_router(semifinished.router, prefix="/semi")
app.include_router(product.router, prefix="/prod")
