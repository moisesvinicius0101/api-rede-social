

from fastapi import APIRouter, HTTPException, status, Depends, Path


router = APIRouter(prefix='/posts', tags=['posts'])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post():
    pass

@router.get("/", status_code=status.HTTP_200_OK)
async def get_posts():
    pass

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_post(id: int = Path(..., gt=0)):
    pass

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int = Path(..., gt=0)):
    pass

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int = Path(..., gt=0)):
    pass

