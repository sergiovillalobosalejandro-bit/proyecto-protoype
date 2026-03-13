from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class History(Base):
    __tablename__ = "history"
    
    id_history = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    intervention_type = Column(String(255), nullable=False)
    description = Column(Text)
    ai_micro = Column(Text, nullable=False)
    date_time = Column(DateTime, nullable=False)
    id_specialist = Column(Integer, ForeignKey("specialist.id_specialist"), nullable=False)
    id_coder = Column(Integer, ForeignKey("coder.id_coder"), nullable=False)
    
    # Relationships
    specialist = relationship("Specialist", back_populates="histories")
    coder = relationship("Coder", back_populates="histories")
    
    def __repr__(self):
        return f"<History(id={self.id_history}, type='{self.intervention_type}', coder_id={self.id_coder})>"
