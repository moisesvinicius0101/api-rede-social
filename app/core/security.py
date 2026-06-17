

import os 
import jwt 
from jwt import InvalidTokenError, ExpiredSignatureError
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status, Depends
# Trocado para HTTPBearer para aceitar login por JSON puro
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# CARREGAMENTO DAS CONFIGURAÇÕES DO .ENV
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


security_scheme = HTTPBearer()

# CONFIGURAÇÃO DA CRIPTOGRAFIA DE SENHA
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- FUNÇÕES DE SENHA ---

def hash_password(password: str) -> str:
    """Transforma a senha em texto puro em um hash seguro."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara a senha digitada com o hash salvo."""
    return pwd_context.verify(plain_password, hashed_password)


# --- FUNÇÕES DE TOKEN (JWT) ---

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Gera um novo Token JWT com tempo de expiração."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
    """Gera um novo Token JWT de refresh com tempo de expiração mais longo."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_tokens(user_id: int) -> dict:
    """Gera um par de tokens (access e refresh) para um usuário autenticado."""
    data = {"sub": str(user_id)}
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    return {"access_token": access_token, "refresh_token": refresh_token}

def validate_refresh_token(token: str) -> dict:
    """Valida o Token de refresh e extrai os dados de dentro dele."""
    credential_exception = {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Could not validate refresh token",
        "headers": {"WWW-Authenticate": "Bearer"},
    }
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject_id: str = payload.get("sub")
        if subject_id is None:
            raise HTTPException(**credential_exception)
        return payload
    except (InvalidTokenError, ExpiredSignatureError):
        raise HTTPException(**credential_exception)
    

def decode_access_token(token: str) -> dict:
    """Valida o Token JWT e extrai os dados de dentro dele."""
    credential_exception = {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Could not validate credentials",
        "headers": {"WWW-Authenticate": "Bearer"},
    }
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject_id: str = payload.get("sub")
        if subject_id is None:
            raise HTTPException(**credential_exception)
        return payload
    except (InvalidTokenError, ExpiredSignatureError):
        raise HTTPException(**credential_exception)

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> int:
    """Extrai o ID do usuário autenticado a partir do token enviado no cabeçalho."""
    # credentials.credentials pega apenas a string do token que você colou
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id: str = payload.get("sub") 
    return int(user_id)