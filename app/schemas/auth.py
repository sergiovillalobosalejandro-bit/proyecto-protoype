from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from ..models import RolUsuario

class UserBase(BaseModel):
    username: str
    email: EmailStr
    nombre_completo: str
    rol: RolUsuario = RolUsuario.TERAPISTA

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    activo: bool
    creado_en: datetime
    
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
