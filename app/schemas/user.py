
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr = Field(..., examples=["user@example.com"])
    full_name: Optional[str] = Field(None, examples=["John Doe"]) 
    bio: Optional[str] = Field(None, examples=["Apaixonado por tecnologia."])
    
class UserCreate(UserBase):
    username: str = Field(..., min_length=3, max_length=50, examples=["johndoe"])
    password: str = Field(..., min_length=6, examples=["strongpassword123"])
    
class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, examples=["John Doe"])
    bio: Optional[str] = Field(None, examples=["Apaixonado por tecnologia e viagens."])
    profile_picture: Optional[str] = Field(None)
    
class UserResponse(UserBase):
    id: int
    username: str
    profile_picture: Optional[str] = None

    model_config = {
        "from_attributes": True
    }