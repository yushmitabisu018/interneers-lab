from pydantic import BaseModel, Field
from typing import List 

class ProductSchema(BaseModel):
    name:str
    brand:str
    price:float=Field(gt=0) # >zero
    quantity:int = Field(ge=0) #>=0

class ProductList(BaseModel):
    products: List[ProductSchema]