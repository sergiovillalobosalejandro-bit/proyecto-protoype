from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import date
from .campus import CampusResponse

class CohortBase(BaseModel):
    name_cohort: str
    start_date: date
    status: str
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        allowed_statuses = ['active', 'inactive', 'completed', 'suspended']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {allowed_statuses}')
        return v

class CohortCreate(CohortBase):
    id_campus: int

class CohortResponse(CohortBase):
    model_config = ConfigDict(from_attributes=True)
    
    id_cohort: int
    id_campus: int
    campus: Optional[CampusResponse] = None

class CohortUpdate(BaseModel):
    name_cohort: Optional[str] = None
    start_date: Optional[date] = None
    status: Optional[str] = None
    id_campus: Optional[int] = None
