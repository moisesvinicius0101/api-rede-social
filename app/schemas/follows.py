

from pydantic import BaseModel, ConfigDict
from datetime import datetime

# O que o usuário envia no corpo da requisição (JSON)
class FollowRequest(BaseModel):
    followed_id: int

# O que a API responde confirmando o vínculo
class FollowResponse(BaseModel):
    id: int
    follower_id: int
    followed_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)