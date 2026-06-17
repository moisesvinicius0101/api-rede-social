

from fastapi import APIRouter, HTTPException, status, Depends, Path, Query, UploadFile, File
from typing import Optional, List
from sqlalchemy.orm import Session
import shutil
import os

from app.database import get_db
from app.models import User
from app.services.users_service import UserService
from app.core.security import get_current_user_id
from app.schemas.user import UserResponse, UserUpdate 

router = APIRouter(prefix='/users', tags=['users'])


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Lista usuários da rede social por filtro."""
    return UserService.get_all(db, skip=skip, limit=limit, name=name)


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Retorna o perfil do usuário que está logado atualmente (baseado no Token)."""
    return UserService.get_by_id(db, user_id=current_user_id)


@router.get("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Busca o perfil de um usuário específico pelo ID."""
    return UserService.get_by_id(db, user_id=id)


@router.put("/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_data: UserUpdate,
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Atualiza dados textuais do perfil (nome, bio, etc)."""
    data_dict = user_data.model_dump(exclude_unset=True) 
    return UserService.update(db, user_id=id, current_user_id=current_user_id, update_data=data_dict)


@router.post("/me/upload-avatar", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def upload_profile_picture(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Faz o upload e atualiza apenas a foto de perfil do usuário logado."""
    # A rota apenas chama o serviço e passa o arquivo bruto
    return UserService.upload_avatar(db, user_id=current_user_id, file=file)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """Exclui a conta do usuário."""
    UserService.delete(db, user_id=id, current_user_id=current_user_id)