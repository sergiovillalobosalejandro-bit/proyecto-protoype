from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class AIReport(Base):
    __tablename__ = "AI_report"
    
    id_reporte = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    period_type = Column(String(255), nullable=False)
    diagnosis = Column(Text, nullable=False)
    risk_level = Column(String(255), nullable=False)
    generated_at = Column(DateTime, nullable=False)
    id_coder = Column(Integer, ForeignKey("coder.id_coder"), nullable=False)
    
    # Relationships
    coder = relationship("Coder", back_populates="ai_reports")
    
    def __repr__(self):
        return f"<AIReport(id={self.id_reporte}, period='{self.period_type}', risk_level='{self.risk_level}')>"
