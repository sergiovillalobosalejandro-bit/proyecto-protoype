from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, TYPE_CHECKING
from datetime import date
from decimal import Decimal

if TYPE_CHECKING:
    from .clan import ClanResponse

class CoderBase(BaseModel):
    full_name: str
    document_id: str
    birth_date: date
    status: str
    withdrawal_date: date
    average: Optional[Decimal] = None
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        allowed_statuses = ['active', 'inactive', 'withdrawn', 'completed', 'suspended']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {allowed_statuses}')
        return v

class CoderCreate(CoderBase):
    id_clan: int

class CoderSimpleResponse(CoderBase):
    model_config = ConfigDict(from_attributes=True)
    
    id_coder: int
    id_clan: int

class CoderResponse(CoderBase):
    model_config = ConfigDict(from_attributes=True)
    
    id_coder: int
    id_clan: int
    clan: Optional[ClanResponse] = None

class CoderUpdate(BaseModel):
    full_name: Optional[str] = None
    document_id: Optional[str] = None
    birth_date: Optional[date] = None
    status: Optional[str] = None
    withdrawal_date: Optional[date] = None
    average: Optional[Decimal] = None
    id_clan: Optional[int] = None

class CoderWithDetails(CoderResponse):
    clan: Optional[ClanResponse] = None
