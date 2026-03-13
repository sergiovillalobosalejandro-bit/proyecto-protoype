from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from .coder import CoderResponse

class LearningPathBase(BaseModel):
    route_type: str
    current_path: int
    clan_average: Optional[Decimal] = None

class LearningPathCreate(LearningPathBase):
    id_coder: int

class LearningPathResponse(LearningPathBase):
    model_config = ConfigDict(from_attributes=True)
    
    id_path: int
    id_coder: int
    coder: Optional[CoderResponse] = None

class LearningPathUpdate(BaseModel):
    route_type: Optional[str] = None
    current_path: Optional[int] = None
    clan_average: Optional[Decimal] = None
    id_coder: Optional[int] = None
