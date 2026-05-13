from pydantic import BaseModel, Field
from typing import List 

class ProductSchema(BaseModel):
    name: str = Field(min_length=1)
    brand: str = Field(min_length=1)
    price: float = Field(gt=0)  # >zero
    quantity: int = Field(ge=0)  # >=0
