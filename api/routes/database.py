from fastapi import APIRouter, HTTPException
router = APIRouter()

database = "Database ('Bot_Discord')"
router.tags = [database]

@router.get("/database", deprecated=True)
async def get_database():
    return {"message": 200}