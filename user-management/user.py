from fastapi import APIRouter, HTTPException
from database import db
from models import UserCreate, UserUpdate
from bson import ObjectId

router = APIRouter()

user_collection = db["users"]

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"]
    }

# Create a new user
@router.post("/create")
def create_user(user: UserCreate):
    # Check if email already exists
    if user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = {
        "username": user.username,
        "email": user.email,
        "password": user.password  # normally you'd hash this!
    }
    result = user_collection.insert_one(new_user)
    return {"id": str(result.inserted_id), "message": "User created successfully"}

# Update user details
@router.put("/update/{user_id}")
def update_user(user_id: str, user: UserUpdate):
    existing_user = user_collection.find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {k: v for k, v in user.dict().items() if v is not None}
    if update_data:
        user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

    return {"message": "User updated successfully"}

# Get all users
@router.get("/all")
def get_all_users():
    users = user_collection.find()
    return [user_helper(user) for user in users]

# Delete a user
@router.delete("/delete/{user_id}")
def delete_user(user_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_collection.delete_one({"_id": ObjectId(user_id)})
    return {"message": "User deleted successfully"}
