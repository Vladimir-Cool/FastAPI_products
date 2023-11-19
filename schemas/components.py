from pydantic import BaseModel, Field


class ComponentsSchemas(BaseModel):
    name: str
    quantity: int = Field(ge=0)
    price: int = Field(ge=0)







