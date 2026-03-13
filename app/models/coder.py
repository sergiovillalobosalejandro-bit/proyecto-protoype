from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class CoderStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    WITHDRAWN = "withdrawn"
    COMPLETED = "completed"
    SUSPENDED = "suspended"

class Coder(Base):
    __tablename__ = "coder"
    
    id_coder = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    full_name = Column(String(150), nullable=False)
    document_id = Column(String(255), unique=True, nullable=False)
    birth_date = Column(Date, nullable=False)
    status = Column(Enum(CoderStatus), nullable=False)
    withdrawal_date = Column(Date, nullable=False)
    average = Column(Numeric(5, 2))
    id_clan = Column(Integer, ForeignKey("clan.id_clan"), nullable=False)
    
    # Relationships
    clan = relationship("Clan", back_populates="coders")
    learning_path = relationship("LearningPath", back_populates="coder", uselist=False)
    histories = relationship("History", back_populates="coder")
    ai_reports = relationship("AIReport", back_populates="coder")
    
    def __repr__(self):
        return f"<Coder(id={self.id_coder}, name='{self.full_name}', status='{self.status.value}')>"
