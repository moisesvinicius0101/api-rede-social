

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.auth import UserRegister, UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:
    
    @staticmethod
    def register_user(user_in: UserRegister, db: Session) -> Token:
        # Verifica se o e-mail já está cadastrado
        email_exists = db.query(User).filter(User.email == user_in.email).first()
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este e-mail já está em uso."
            )
            
        # Verifica se o username já está cadastrado
        username_exists = db.query(User).filter(User.username == user_in.username).first()
        if username_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este nome de usuário já está em uso."
            )
            
        # Faz o hash da senha e cria o modelo do banco
        hashed_pwd = hash_password(user_in.password)
        new_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_pwd
        )
        
        # Salva no db
        db.add(new_user)
        db.commit()
        db.refresh(new_user) # Recarrega o objeto para pegar o ID gerado pelo Postgres
        
        # Gera o token passando o ID como string no 'sub'
        access_token = create_access_token(data={"sub": str(new_user.id)})
        
        return Token(access_token=access_token, token_type="bearer")

    @staticmethod
    def authenticate_user(user_in: UserLogin, db: Session) -> Token:
        # Busca o usuário pelo e-mail
        user = db.query(User).filter(User.email == user_in.email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Verifica se a senha bate com o hash do banco
        if not verify_password(user_in.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Se deu tudo certo, gera o token com o ID
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return Token(access_token=access_token, token_type="bearer")