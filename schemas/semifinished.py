from typing import Dict, List
from pydantic import BaseModel, Field


class ComponentDict(BaseModel):
    component_id: int
    count: int = Field(ge=0)


class SemifinishedSchemas(BaseModel):
    name: str
    quantity: int = Field(ge=0)
    price: int = Field(ge=0)
    components: List[ComponentDict]
