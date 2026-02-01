from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    nome: str

class UserCreate(UserBase):
    senha: str

class UserUpdate(UserBase):
    senha: Optional[str] = None

class User(UserBase):
    id_usuario: int

    class Config:
        from_attributes = True
