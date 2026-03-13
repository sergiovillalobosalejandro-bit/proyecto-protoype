from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..core.database import Base

class Campus(Base):
    __tablename__ = "campus"
    
    id_campus = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    campus_name = Column(String(255), nullable=False)
    
    # Relationships
    cohorts = relationship("app.models.cohort.Cohort", back_populates="campus")
    
    def __repr__(self):
        return f"<Campus(id={self.id_campus}, name='{self.campus_name}')>"
