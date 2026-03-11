from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Intervencion(Base):
    __tablename__ = "intervenciones"
    
    id = Column(Integer, primary_key=True, index=True)
    couder_id = Column(Integer, ForeignKey("couders.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    titulo = Column(String, nullable=False)
    descripcion = Column(Text, nullable=False)
    observaciones = Column(Text)
    fecha_intervencion = Column(DateTime(timezone=True), nullable=False)
    duracion_minutos = Column(Integer)
    tipo_intervencion = Column(String)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    usuario = relationship("Usuario", backref="intervenciones")
