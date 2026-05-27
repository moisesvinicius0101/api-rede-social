
from fastapi import APIRouter, HTTPException, status, Depends, Path, Query 
from typing import Optional
# Exemplo de importação do seu core/security (ajuste conforme suas pastas)
# from app.core.security import get_current_user 

router = APIRouter(prefix='/users', tags=['users'])

# Essa rota vai páginação e filtração por nome
@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    name: Optional[str] = Query(None)
):
    """
    Lista usuários da rede social por filtro.
    """
    pass

@router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user_profile():
    """
    Retorna o perfil do usuário que está logado atualmente (baseado no Token).
    """
    pass

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_user(id: int = Path(..., gt=0)):
    """
    Busca o perfil de um usuário específico pelo ID (quando você clica no perfil de alguém).
    """
    pass

@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_user(id: int = Path(..., gt=0)):
    """
    Atualiza os dados do usuário (Bio, Nome, Foto). 
    Regra de negócio: Um usuário só pode atualizar o seu próprio ID.
    """
    pass

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int = Path(..., gt=0)):
    """
    Exclui a conta do usuário.
    Regra de negócio: Um usuário só pode deletar a sua própria conta.
    """
    pass