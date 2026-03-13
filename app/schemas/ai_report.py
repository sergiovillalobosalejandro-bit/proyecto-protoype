from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
from .coder import CoderResponse

class AIReportBase(BaseModel):
    period_type: str
    diagnosis: str
    risk_level: str
    generated_at: datetime
    
    @field_validator('risk_level')
    @classmethod
    def validate_risk_level(cls, v):
        allowed_levels = ['low', 'medium', 'high', 'critical']
        if v.lower() not in allowed_levels:
            raise ValueError(f'Risk level must be one of: {allowed_levels}')
        return v.lower()

class AIReportCreate(AIReportBase):
    id_coder: int

class AIReportResponse(AIReportBase):
    model_config = ConfigDict(from_attributes=True)
    
    id_reporte: int
    id_coder: int
    coder: Optional[CoderResponse] = None

class AIReportUpdate(BaseModel):
    period_type: Optional[str] = None
    diagnosis: Optional[str] = None
    risk_level: Optional[str] = None
    generated_at: Optional[datetime] = None
    id_coder: Optional[int] = None
