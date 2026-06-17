

import os
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app.models.user import User, RefreshToken 
from app.schemas.auth import UserRegister, UserLogin, Token
from app.core.security import hash_password, verify_password, create_tokens 

# Pode ser configurado via variável de ambiente ou usar um valor padrão
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

class AuthService:
    
    @staticmethod
    def register_user(user_in: UserRegister, db: Session) -> Token:
        # validações existentes de e-mail e username 
        email_exists = db.query(User).filter(User.email == user_in.email).first()
        if email_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este e-mail já está em uso.")
            
        username_exists = db.query(User).filter(User.username == user_in.username).first()
        if username_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este nome de usuário já está em uso.")
            
        # Criação do Usuário 
        hashed_pwd = hash_password(user_in.password)
        new_user = User(username=user_in.username, email=user_in.email, hashed_password=hashed_pwd)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Gerar o PAR de tokens usando a função nova
        tokens_dict = create_tokens(user_id=new_user.id)
        
        # Salvar o refresh token gerado no banco de dados
        db_refresh = RefreshToken(
            user_id=new_user.id,
            token=tokens_dict["refresh_token"],
            expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(db_refresh)
        db.commit() # Salva o token no banco
        
        # Retorna o schema com os dois tokens
        return Token(
            access_token=tokens_dict["access_token"], 
            refresh_token=tokens_dict["refresh_token"], 
            token_type="bearer"
        )

    @staticmethod
    def authenticate_user(user_in: UserLogin, db: Session) -> Token:
        # validações de login existentes (mantém igual)
        user = db.query(User).filter(User.email == user_in.email).first()
        if not user or not verify_password(user_in.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Gerar o PAR de tokens para o login bem-sucedido
        tokens_dict = create_tokens(user_id=user.id)
        
        # Salvar o refresh token no banco de dados
        db_refresh = RefreshToken(
            user_id=user.id,
            token=tokens_dict["refresh_token"],
            expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        db.add(db_refresh)
        db.commit()
        
        # Retorna o schema com os dois tokens
        return Token(
            access_token=tokens_dict["access_token"], 
            refresh_token=tokens_dict["refresh_token"], 
            token_type="bearer"
        )
        
    @staticmethod
    def logout_user(refresh_token: str, db: Session):
        # Busca o token no banco
        db_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
        
        # Se o token existir, a gente invalida ele
        if db_token:
            db_token.is_revoked = True
            db.commit()
            
        return {"detail": "Logout realizado com sucesso."}