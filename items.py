# items.py

from fastapi import APIRouter, HTTPException
from database import db  # Assuming the database connection is in `database.py`
from models import ItemCreate, ItemUpdate
from bson import ObjectId  # For converting ObjectId from MongoDB

router = APIRouter()

items_collection = db["items"] 

def item_helper(item) -> dict:
    """Helper function to format item data from MongoDB"""
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "price": item["price"]
    }

# Add a new item to the catalog
@router.post("/items/add")
def add_item(item: ItemCreate):
    new_item = {
        "name": item.name,
        "price": item.price
    }
    result = items_collection.insert_one(new_item)
    return {"id": str(result.inserted_id), "message": "Item added successfully"}

# Update an existing item
@router.put("/items/update/{item_id}")
def update_item(item_id: str, item: ItemUpdate):
    item_to_update = items_collection.find_one({"_id": ObjectId(item_id)})
    
    if not item_to_update:
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated_item = {
        "name": item.name,
        "price": item.price
    }
    
    items_collection.update_one({"_id": ObjectId(item_id)}, {"$set": updated_item})
    
    return {"message": "Item updated successfully"}

# Delete an item by its ID
@router.delete("/items/delete/{item_id}")
def delete_item(item_id: str):
    item_to_delete = items_collection.find_one({"_id": ObjectId(item_id)})
    
    if not item_to_delete:
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_collection.delete_one({"_id": ObjectId(item_id)})
    return {"message": "Item deleted successfully"}

# Get all items in the catalog
@router.get("/items")
def get_items():
    items = items_collection.find()
    return [item_helper(item) for item in items]
