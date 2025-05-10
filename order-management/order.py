from fastapi import APIRouter, HTTPException
from database import db
from models import OrderCreate, OrderUpdate
from bson import ObjectId

router = APIRouter()

order_collection = db["orders"]

def order_helper(order) -> dict:
    return {
        "id": str(order["_id"]),
        "user_id": order["user_id"],
        "items": order["items"],
        "status": order["status"]
    }

# Create a new order
@router.post("/create")
def create_order(order: OrderCreate):
    new_order = {
        "user_id": order.user_id,
        "items": [{"item_id": item.item_id, "quantity": item.quantity} for item in order.items],
        "status": "pending"  # default status
    }
    result = order_collection.insert_one(new_order)
    return {"id": str(result.inserted_id), "message": "Order created successfully"}

# Update an order status
@router.put("/update/{order_id}")
def update_order(order_id: str, order: OrderUpdate):
    existing_order = order_collection.find_one({"_id": ObjectId(order_id)})

    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    order_collection.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": order.status}})
    return {"message": "Order updated successfully"}

# Get orders by user_id
@router.get("/user/{user_id}")
def get_orders_by_user(user_id: str):
    orders = order_collection.find({"user_id": user_id})
    return [order_helper(order) for order in orders]

# Delete an order
@router.delete("/delete/{order_id}")
def delete_order(order_id: str):
    order = order_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order_collection.delete_one({"_id": ObjectId(order_id)})
    return {"message": "Order deleted successfully"}
