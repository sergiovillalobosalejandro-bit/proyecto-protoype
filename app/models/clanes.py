from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class Jornada(enum.Enum):
    AM = "AM"
    PM = "PM"

class Clan(Base):
    __tablename__ = "clanes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    corte_id = Column(Integer, ForeignKey("cortes.id"), nullable=False)
    jornada = Column(Enum(Jornada), nullable=False)
    capacidad_maxima = Column(Integer, default=30)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    couders = relationship("Couder", backref="clan")
