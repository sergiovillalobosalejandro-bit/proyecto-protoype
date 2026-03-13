from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class CohortStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"
    SUSPENDED = "suspended"

class Cohort(Base):
    __tablename__ = "cohort"
    
    id_cohort = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name_cohort = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    status = Column(Enum(CohortStatus), nullable=False)
    id_campus = Column(Integer, ForeignKey("campus.id_campus"), nullable=False)
    
    # Relationships
    campus = relationship("app.models.campus.Campus", back_populates="cohorts")
    clans = relationship("app.models.clan.Clan", back_populates="cohort")
    
    def __repr__(self):
        return f"<Cohort(id={self.id_cohort}, name='{self.name_cohort}', status='{self.status.value}')>"
