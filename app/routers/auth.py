
from fastapi import APIRouter, HTTPException, status, Depends 
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated

from app.schemas.auth import Token, UserLogin, UserRegister, RefreshToken
from app.services.auth_service import AuthService
from app.core.security import validate_refresh_token, create_access_token
from app.models.user import RefreshToken as RefreshTokenModel

router = APIRouter(prefix='/auth', tags=['auth'])

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token) 
async def login(user_in: UserLogin, db: db_dependency):
    """
    Recebe as credenciais (e-mail e senha), 
    valida no banco e retorna os tokens de acesso e refresh.
    """
    return AuthService.authenticate_user(user_in, db)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=Token)
async def register(user_in: UserRegister, db: db_dependency):
    """
    Recebe os dados do novo usuário, faz o hash da senha, 
    salva no banco de dados e retorna os tokens de acesso e refresh.
    """
    return AuthService.register_user(user_in, db)


@router.post("/refresh", response_model=Token)
async def refresh_access_token(body: RefreshToken, db: db_dependency): 
    # Valida o JWT do refresh token e extrai o payload
    payload = validate_refresh_token(body.refresh_token)
    user_id = payload.get("sub")
    
    # Verifica se o token realmente existe gravado no banco de dados
    db_token = db.query(RefreshTokenModel).filter(RefreshTokenModel.token == body.refresh_token).first()
    if not db_token or db_token.is_revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou já revogado."
        )
    
    # Se passou nas validações, gera apenas um NOVO access_token
    new_access_token = create_access_token(data={"sub": str(user_id)})
    
    # Devolve o novo access_token mantendo o mesmo refresh_token que ele usou
    return Token(
        access_token=new_access_token,
        refresh_token=body.refresh_token,
        token_type="bearer"
    )
    
@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(body: RefreshToken, db: db_dependency):
    """
    Invalida o refresh token enviado, deslogando o usuário do dispositivo.
    """
    return AuthService.logout_user(body.refresh_token, db)