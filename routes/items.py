from fastapi import APIRouter
from schema import DNATaskCreate, DNATask

router = APIRouter()

@router.get("/")
def test_route():
    return {"message": "Items route is working!"}