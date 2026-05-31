

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.schemas.follows import FollowRequest, FollowResponse
from app.services.follows_service import FollowService
from app.database import get_db  
from app.core.security import get_current_user_id

router = APIRouter(prefix='/follows', tags=['follows'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=FollowResponse)
async def follow_user(
    body: FollowRequest, 
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Faz o usuário logado seguir outro usuário com base no followed_id enviado no JSON.
    """
    return FollowService.follow_user(
        db=db, 
        follower_id=current_user_id, 
        followed_id=body.followed_id
    )

@router.delete("/{followed_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(
    followed_id: int, 
    db: Session = Depends(get_db), 
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Faz o usuário logado deixar de seguir o usuário do ID passado na URL.
    """
    FollowService.unfollow_user(
        db=db, 
        follower_id=current_user_id, 
        followed_id=followed_id
    )
    return None