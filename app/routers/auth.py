

from fastapi import APIRouter, HTTPException, status, Depends 


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/login", status_code=status.HTTP_200_OK) 
async def register():
    pass 

@router.post("/register", status_code=status.HTTP_200_OK)
async def register():
    pass 