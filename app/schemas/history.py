from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from .specialist import SpecialistResponse
from .coder import CoderResponse

class HistoryBase(BaseModel):
    intervention_type: str
    description: Optional[str] = None
    ai_micro: str
    date_time: datetime

class HistoryCreate(HistoryBase):
    id_specialist: int
    id_coder: int

class HistoryResponse(HistoryBase):
    model_config = ConfigDict(from_attributes=True)
    
    id_history: int
    id_specialist: int
    id_coder: int
    specialist: Optional[SpecialistResponse] = None
    coder: Optional[CoderResponse] = None

class HistoryUpdate(BaseModel):
    intervention_type: Optional[str] = None
    description: Optional[str] = None
    ai_micro: Optional[str] = None
    date_time: Optional[datetime] = None
    id_specialist: Optional[int] = None
    id_coder: Optional[int] = None
