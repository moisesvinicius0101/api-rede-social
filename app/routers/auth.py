

from fastapi import APIRouter, HTTPException, status, Depends 
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated
from app.schemas import Token, TokenData, UserLogin, UserRegister
from app.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['auth'])

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token) 
async def login(user_in: UserLogin, db: db_dependency):
    """
    Recebe as credenciais (username/e-mail e senha), 
    valida no banco e retorna o token de acesso.
    """
    return AuthService.authenticate_user(user_in, db)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=Token)
async def register(user_in: UserRegister, db: db_dependency):
    """
    Recebe os dados do novo usuário, faz o hash da senha, 
    salva no banco de dados e já pode retornar o token de login.
    """
    return AuthService.register_user(user_in, db)