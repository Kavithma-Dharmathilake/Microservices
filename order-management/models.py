from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    item_id: str
    quantity: int

class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]

class OrderUpdate(BaseModel):
    status: str  # e.g., "pending", "shipped", "delivered"
