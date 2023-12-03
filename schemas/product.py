from typing import Dict, List, Union
from pydantic import BaseModel, Field

from schemas.components import ComponentsSchemas


class ComponentDict(BaseModel):
    component_id: int
    count: int = Field(ge=0)


class SemiFinishedDict(BaseModel):
    semifinished_id: int
    count: int = Field(ge=0)


class ProductDict(BaseModel):
    product_id: int
    count: int = Field(ge=0)


class ProductSchemas(BaseModel):
    name: str
    quantity: int = Field(ge=0)
    price: int = Field(ge=0)
    component_list: Union[List[ComponentDict], None]
    semifinished_list: Union[List[SemiFinishedDict], None]
    product_list: Union[List[ProductDict], None]
