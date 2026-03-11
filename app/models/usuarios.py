from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from ..core.database import Base
import enum

class RolUsuario(enum.Enum):
    ADMIN = "admin"
    TERAPISTA = "terapista"
    COORDINADOR = "coordinador"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    nombre_completo = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    rol = Column(Enum(RolUsuario), default=RolUsuario.TERAPISTA)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())
