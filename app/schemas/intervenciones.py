from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class IntervencionBase(BaseModel):
    couder_id: int
    usuario_id: int
    titulo: str
    descripcion: str
    observaciones: Optional[str] = None
    fecha_intervencion: datetime
    duracion_minutos: Optional[int] = None
    tipo_intervencion: Optional[str] = None

class IntervencionCreate(IntervencionBase):
    pass

class IntervencionUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    observaciones: Optional[str] = None
    fecha_intervencion: Optional[datetime] = None
    duracion_minutos: Optional[int] = None
    tipo_intervencion: Optional[str] = None

class IntervencionResponse(IntervencionBase):
    id: int
    creado_en: datetime
    actualizado_en: Optional[datetime] = None
    
    model_config = {"from_attributes": True}

class AudioRecordBase(BaseModel):
    couder_id: int
    usuario_id: int
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    intervencion_id: Optional[int] = None
    archivo_path: str
    duracion_segundos: Optional[int] = None
    tamano_bytes: int

class AudioRecordCreate(AudioRecordBase):
    pass

class AudioRecordResponse(AudioRecordBase):
    id: Optional[str] = None
    fecha_grabacion: datetime
    transcricion: Optional[str] = None
    analisis_ai: Optional[Dict[str, Any]] = None
    
    model_config = {"from_attributes": True}

class ClinicalHistoryRecord(BaseModel):
    _id: Optional[str] = None
    couder_id: int
    intervencion_id: int
    notas_completas: str
    sintomas_observados: List[str]
    estado_emocional: str
    nivel_participacion: str
    observaciones_adicionales: str
    fecha_registro: datetime
    actualizado_en: Optional[datetime] = None
