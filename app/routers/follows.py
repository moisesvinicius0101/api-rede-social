

from fastapi import APIRouter, HTTPException, status, Depends 


router = APIRouter(prefix="/follows", tags=['follows'])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def follow_user():
    pass

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user():
    pass

