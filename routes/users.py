from fastapi import APIRouter

# This is the "attribute" main.py is looking for
router = APIRouter()

@router.get("/")
def get_users():
    return {"message": "User routes connected"}