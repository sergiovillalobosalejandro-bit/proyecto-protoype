from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class EstadoCouder(enum.Enum):
    ACTIVO = "activo"
    RETIRADO = "retirado"
    COMPLETADO = "completado"

class Couder(Base):
    __tablename__ = "couders"
    
    id = Column(Integer, primary_key=True, index=True)
    cc = Column(String, nullable=False, unique=True, index=True)
    nombre_completo = Column(String, nullable=False)
    fecha_nacimiento = Column(Date)
    telefono = Column(String)
    email = Column(String)
    direccion = Column(String)
    clan_id = Column(Integer, ForeignKey("clanes.id"), nullable=False)
    estado = Column(Enum(EstadoCouder), default=EstadoCouder.ACTIVO)
    fecha_ingreso = Column(DateTime(timezone=True), server_default=func.now())
    fecha_retiro = Column(DateTime(timezone=True), nullable=True)
    fecha_completado = Column(DateTime(timezone=True), nullable=True)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    intervenciones = relationship("Intervencion", backref="couder")
