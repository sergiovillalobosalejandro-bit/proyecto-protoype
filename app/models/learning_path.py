from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class LearningPath(Base):
    __tablename__ = "learning_path"
    
    id_path = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    route_type = Column(String(255), nullable=False)
    current_path = Column(Integer, nullable=False)
    clan_average = Column(Numeric(5, 2))
    id_coder = Column(Integer, ForeignKey("coder.id_coder"), unique=True, nullable=False)
    
    # Relationships
    coder = relationship("Coder", back_populates="learning_path")
    
    def __repr__(self):
        return f"<LearningPath(id={self.id_path}, type='{self.route_type}', coder_id={self.id_coder})>"
