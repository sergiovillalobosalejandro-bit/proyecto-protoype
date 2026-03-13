from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..core.database import Base

class Specialist(Base):
    __tablename__ = "specialist"
    
    id_specialist = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name_specialist = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    # Relationships
    histories = relationship("History", back_populates="specialist")
    
    def __repr__(self):
        return f"<Specialist(id={self.id_specialist}, name='{self.name_specialist}', email='{self.email}')>"
