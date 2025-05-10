from pydantic import BaseModel
from typing import List

class CartItem(BaseModel):
    item_id: str
    quantity: int

class CartCreate(BaseModel):
    user_id: str
    items: List[CartItem]

class CartUpdate(BaseModel):
    items: List[CartItem]
