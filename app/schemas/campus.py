from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CampusBase(BaseModel):
    campus_name: str

class CampusCreate(CampusBase):
    pass

class CampusResponse(CampusBase):
    model_config = ConfigDict(from_attributes=True)
    
    id_campus: int

class CampusUpdate(BaseModel):
    campus_name: Optional[str] = None
