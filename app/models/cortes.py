from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class TipoRuta(enum.Enum):
    BASICA = "basica"
    AVANZADA = "avanzada"

class Corte(Base):
    __tablename__ = "cortes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    sede_id = Column(Integer, ForeignKey("sedes.id"), nullable=False)
    fecha_inicio = Column(DateTime(timezone=True), nullable=False)
    fecha_fin = Column(DateTime(timezone=True), nullable=False)
    tipo_ruta = Column(Enum(TipoRuta), nullable=False)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sede = relationship("Sede", backref="cortes")
    clanes = relationship("Clan", backref="corte")
