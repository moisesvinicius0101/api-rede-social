

import os 
import jwt 
from jwt import InvalidTokenError, ExpiredSignatureError
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

# CARREGAMENTO DAS CONFIGURAÇÕES DO .ENV
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login") 

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

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Extrai o ID do usuário autenticado a partir do token."""
    payload = decode_access_token(token)
    user_id: str = payload.get("sub") 
    return int(user_id)