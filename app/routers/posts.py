
from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlalchemy.orm import Session
from typing import List

from app.schemas.post import PostCreate, PostResponse
from app.services.posts_service import PostService
from app.database import get_db  
from app.core.security import get_current_user_id

router = APIRouter(prefix='/posts', tags=['posts'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(post_data: PostCreate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return PostService.create(db, post_data, current_user_id)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    return PostService.get_all(db)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def get_post(id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    return PostService.get_by_id(db, id)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
async def update_post(post_data: PostCreate, id: int = Path(..., gt=0), db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    return PostService.update(db, id, post_data, current_user_id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int = Path(..., gt=0), db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    PostService.delete(db, id, current_user_id)
    return None