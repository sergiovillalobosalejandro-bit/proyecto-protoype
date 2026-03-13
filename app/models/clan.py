from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class Shift(enum.Enum):
    MORNING = "morning"
    AFTERNOON = "afternoon"
    NIGHT = "night"
    FULL_TIME = "full_time"

class Clan(Base):
    __tablename__ = "clan"
    
    id_clan = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name_clan = Column(String(255), nullable=False)
    shift = Column(Enum(Shift), nullable=False)
    id_cohort = Column(Integer, ForeignKey("cohort.id_cohort"), nullable=False)
    
    # Relationships
    cohort = relationship("app.models.cohort.Cohort", back_populates="clans")
    coders = relationship("app.models.coder.Coder", back_populates="clan")
    
    def __repr__(self):
        return f"<Clan(id={self.id_clan}, name='{self.name_clan}', shift='{self.shift.value}')>"
