

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User
from typing import Optional

class UserService:
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, name: Optional[str] = None):
        query = db.query(User)
        # Se enviaram um nome no filtro, busca usando LIKE (ignorando maiúsculas/minúsculas)
        if name:
            query = query.filter(User.username.ilike(f"%{name}%"))
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )
        return user

    @staticmethod
    def update(db: Session, user_id: int, current_user_id: int, update_data: dict):
        # Regra de negócio: impede o usuário de editar o perfil dos outros
        if user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para alterar o perfil de outro usuário."
            )
        
        user = UserService.get_by_id(db, user_id)
        
        # Atualiza apenas os campos enviados (ex: bio, nome, etc.)
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)
                
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: int, current_user_id: int):
        # Regra de negócio: impede o usuário de deletar a conta dos outros
        if user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para deletar a conta de outro usuário."
            )
            
        user = UserService.get_by_id(db, user_id)
        db.delete(user)
        db.commit()