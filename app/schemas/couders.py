from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime, date
import re
from ..models import EstadoCouder, Corte, Sede, LegacyClan

class CouderBase(BaseModel):
    cc: str
    nombre_completo: str
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    clan_id: int
    
    @field_validator('cc')
    @classmethod
    def validate_cc(cls, v):
        if not re.match(r'^\d{6,12}$', v):
            raise ValueError('CC debe contener solo números (6-12 dígitos)')
        return v
    
    @field_validator('nombre_completo')
    @classmethod
    def validate_nombre_completo(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Nombre completo debe tener al menos 3 caracteres')
        return v.strip()
    
    @field_validator('telefono')
    @classmethod
    def validate_telefono(cls, v):
        if v and not re.match(r'^\d{7,15}$', v):
            raise ValueError('Teléfono debe contener solo números (7-15 dígitos)')
        return v

class CouderCreate(CouderBase):
    estado: EstadoCouder = EstadoCouder.ACTIVO

class CouderUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    estado: Optional[EstadoCouder] = None
    clan_id: Optional[int] = None

class CouderResponse(CouderBase):
    id: int
    estado: EstadoCouder
    fecha_ingreso: datetime
    fecha_retiro: Optional[datetime] = None
    fecha_completado: Optional[datetime] = None
    activo: bool
    creado_en: datetime
    
    model_config = {"from_attributes": True}

class ClanBase(BaseModel):
    id: int
    nombre: str
    jornada: str
    capacidad_maxima: int
    
    model_config = {"from_attributes": True}

class CorteBase(BaseModel):
    id: int
    nombre: str
    tipo_ruta: str
    fecha_inicio: datetime
    fecha_fin: datetime
    
    model_config = {"from_attributes": True}

class SedeBase(BaseModel):
    id: int
    nombre: str
    direccion: str
    telefono: str
    email: str
    
    model_config = {"from_attributes": True}

class CouderWithDetails(CouderResponse):
    clan: Optional[ClanBase] = None
    corte: Optional[CorteBase] = None
    sede: Optional[SedeBase] = None
    
    model_config = {"from_attributes": True}
