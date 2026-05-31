


from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.follow import Follow 
from app.models.user import User

class FollowService:

    @staticmethod
    def follow_user(db: Session, follower_id: int, followed_id: int):
        # Não pode seguir a si mesmo
        if follower_id == followed_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você não pode seguir a si mesmo."
            )
            
        # Verificar se o usuário que será seguido realmente existe
        user_to_follow = db.query(User).filter(User.id == followed_id).first()
        if not user_to_follow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="O usuário que você tentou seguir não existe."
            )
        
        # RVerificar se já segue
        already_following = db.query(Follow).filter(
            Follow.follower_id == follower_id,
            Follow.followed_id == followed_id
        ).first()
        
        if already_following:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Você já segue este usuário."
            )
        
        # Se passou por tudo, cria o vínculo
        new_follow = Follow(follower_id=follower_id, followed_id=followed_id)
        db.add(new_follow)
        db.commit()
        db.refresh(new_follow)
        return new_follow

    @staticmethod
    def unfollow_user(db: Session, follower_id: int, followed_id: int):
        # Busca o vínculo de seguidor
        follow_record = db.query(Follow).filter(
            Follow.follower_id == follower_id,
            Follow.followed_id == followed_id
        ).first()
        
        # Se não encontrar, gera erro
        if not follow_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Você não segue este usuário."
            )
        
        # Deleta o registro (remove o vínculo)
        db.delete(follow_record)
        db.commit()
        return