# cart.py

from fastapi import APIRouter, HTTPException
from database import db
from models import CartCreate, CartUpdate
from bson import ObjectId

router = APIRouter()

cart_collection = db["cart"]

def cart_helper(cart) -> dict:
    return {
        "id": str(cart["_id"]),
        "user_id": cart["user_id"],
        "items": cart["items"],
    }

# Create a new cart
@router.post("/create")
def create_cart(cart: CartCreate):
    new_cart = {
        "user_id": cart.user_id,
        "items": [{"item_id": item.item_id, "quantity": item.quantity} for item in cart.items]
    }
    result = cart_collection.insert_one(new_cart)
    return {"id": str(result.inserted_id), "message": "Cart created successfully"}

# Update an existing cart
@router.put("/update/{cart_id}")
def update_cart(cart_id: str, cart: CartUpdate):
    existing_cart = cart_collection.find_one({"_id": ObjectId(cart_id)})

    if not existing_cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    updated_cart = {
        "items": [{"item_id": item.item_id, "quantity": item.quantity} for item in cart.items]
    }

    cart_collection.update_one({"_id": ObjectId(cart_id)}, {"$set": updated_cart})
    return {"message": "Cart updated successfully"}

# Get a cart by user_id
@router.get("/user/{user_id}")
def get_cart_by_user(user_id: str):
    cart = cart_collection.find_one({"user_id": user_id})
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart_helper(cart)

# Delete a cart
@router.delete("/delete/{cart_id}")
def delete_cart(cart_id: str):
    cart = cart_collection.find_one({"_id": ObjectId(cart_id)})
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart_collection.delete_one({"_id": ObjectId(cart_id)})
    return {"message": "Cart deleted successfully"}
