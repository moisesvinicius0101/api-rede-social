

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.post import Post
from app.schemas.post import PostCreate

class PostService:
    
    @staticmethod
    def create(db: Session, post_data: PostCreate, current_user_id: int):
        new_post = Post(
            content=post_data.content,
            image_url=post_data.image_url,
            user_id=current_user_id
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        # Retorna apenas posts ativos 
        return db.query(Post).filter(Post.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, post_id: int):
        post = db.query(Post).filter(Post.id == post_id, Post.is_active == True).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Post não encontrado"
            )
        return post

    @staticmethod
    def update(db: Session, post_id: int, post_data: PostCreate, current_user_id: int):
        post = PostService.get_by_id(db, post_id)
        
        # Validação crucial: o usuário logado é o dono do post?
        if post.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Você não tem permissão para atualizar este post"
            )
            
        post.content = post_data.content
        post.image_url = post_data.image_url
        
        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def delete(db: Session, post_id: int, current_user_id: int):
        post = PostService.get_by_id(db, post_id)
        
        # Validação crucial: o usuário logado é o dono do post?
        if post.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Você não tem permissão para deletar este post"
            )
            
        # Em vez de apagar do banco, faz "Soft Delete" mudando is_active para False
        post.is_active = False
        db.commit()
        return