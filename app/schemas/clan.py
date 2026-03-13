from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
from .cohort import CohortResponse

class ClanBase(BaseModel):
    name_clan: str
    shift: str
    
    @field_validator('shift')
    @classmethod
    def validate_shift(cls, v):
        allowed_shifts = ['morning', 'afternoon', 'night', 'full_time']
        if v not in allowed_shifts:
            raise ValueError(f'Shift must be one of: {allowed_shifts}')
        return v

class ClanCreate(ClanBase):
    id_cohort: int

class ClanResponse(ClanBase):
    model_config = ConfigDict(from_attributes=True)
    
    id_clan: int
    id_cohort: int
    cohort: Optional[CohortResponse] = None

class ClanUpdate(BaseModel):
    name_clan: Optional[str] = None
    shift: Optional[str] = None
    id_cohort: Optional[int] = None

class ClanWithCoders(ClanResponse):
    coders: Optional[List['CoderResponse']] = []
