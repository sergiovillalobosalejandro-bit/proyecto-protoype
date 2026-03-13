from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from typing import Optional

class SpecialistBase(BaseModel):
    name_specialist: str
    email: EmailStr
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class SpecialistCreate(SpecialistBase):
    pass

class SpecialistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id_specialist: int
    name_specialist: str
    email: EmailStr

class SpecialistUpdate(BaseModel):
    name_specialist: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
