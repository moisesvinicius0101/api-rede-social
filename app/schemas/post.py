

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# O que o usuário envia ao criar/atualizar um post
class PostCreate(BaseModel):
    content: str
    image_url: Optional[str] = None

# O que a API retorna ao consultar um post
class PostResponse(BaseModel):
    id: int
    content: str
    image_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int
    
    # Permite que o Pydantic leia os dados diretamente do modelo do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)