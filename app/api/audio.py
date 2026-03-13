from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime
from pathlib import Path
from ..core.database import get_db
from ..core.mongodb import get_mongo_db
from ..core.logging import logger
from ..models import Couder, Usuario, Intervencion
from ..schemas.intervenciones import AudioRecordResponse, AudioRecordCreate

router = APIRouter()

# Audio storage directory
AUDIO_STORAGE_DIR = "audio_files"
os.makedirs(AUDIO_STORAGE_DIR, exist_ok=True)

@router.post("/upload", response_model=AudioRecordResponse, status_code=status.HTTP_201_CREATED)
async def upload_audio(
    couder_id: int,
    usuario_id: int,
    titulo: Optional[str] = None,
    descripcion: Optional[str] = None,
    intervencion_id: Optional[int] = None,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    """Upload audio recording for a couder"""
    
    # Verify couder exists
    couder = db.query(Couder).filter(Couder.id == couder_id, Couder.activo == True).first()
    if not couder:
        raise HTTPException(status_code=404, detail="Couder not found")
    
    # Verify user exists
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id, Usuario.activo == True).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify intervention exists if provided
    if intervencion_id:
        intervencion = db.query(Intervencion).filter(Intervencion.id == intervencion_id).first()
        if not intervencion:
            raise HTTPException(status_code=404, detail="Intervention not found")
    
    # Validate audio file
    if not file.content_type.startswith('audio/'):
        logger.log_security_event(
            event="INVALID_FILE_TYPE",
            user_id=usuario_id,
            details=f"Attempted to upload non-audio file: {file.content_type}"
        )
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    # Check file size (max 50MB)
    max_size = 50 * 1024 * 1024  # 50MB in bytes
    file_content = await file.read()
    if len(file_content) > max_size:
        logger.log_security_event(
            event="FILE_TOO_LARGE",
            user_id=usuario_id,
            details=f"Attempted to upload file of size: {len(file_content)} bytes"
        )
        raise HTTPException(status_code=400, detail="File size must be less than 50MB")
    
    # Reset file pointer
    await file.seek(0)
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'wav'
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(AUDIO_STORAGE_DIR, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        file_size = os.path.getsize(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save audio file: {str(e)}")
    
    # Create audio record in MongoDB
    audio_record = {
        "couder_id": couder_id,
        "usuario_id": usuario_id,
        "intervencion_id": intervencion_id,
        "titulo": titulo or f"Audio recording {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        "descripcion": descripcion or "",
        "archivo_path": file_path,
        "duracion_segundos": None,  # Will be updated when processed
        "formato": file_extension,
        "tamano_bytes": file_size,
        "transcripcion": None,
        "fecha_grabacion": datetime.utcnow(),
        "fecha_transcripcion": None,
        "estado": "grabado",
        "metadata": {
            "calidad_audio": "unknown",
            "dispositivo_grabacion": "web",
            "ubicacion": "unknown"
        }
    }
    
    result = mongo_db.audio_registros.insert_one(audio_record)
    
    return {
        "id": str(result.inserted_id),
        "message": "Audio uploaded successfully",
        "filename": unique_filename,
        "file_size": file_size
    }

@router.get("/couder/{couder_id}")
async def get_audio_by_couder(
    couder_id: int,
    limit: int = 50,
    mongo_db = Depends(get_mongo_db)
):
    """Get audio recordings for a couder"""
    
    # Verify couder exists
    couder = db.query(Couder).filter(Couder.id == couder_id, Couder.activo == True).first()
    if not couder:
        raise HTTPException(status_code=404, detail="Couder not found")
    
    recordings = list(mongo_db.audio_registros.find(
        {"couder_id": couder_id}
    ).sort("fecha_grabacion", -1).limit(limit))
    
    # Convert ObjectId to string and format response
    for recording in recordings:
        if "_id" in recording:
            recording["_id"] = str(recording["_id"])
        if "fecha_grabacion" in recording:
            recording["fecha_grabacion"] = recording["fecha_grabacion"].isoformat()
        if "fecha_transcripcion" in recording and recording["fecha_transcripcion"]:
            recording["fecha_transcripcion"] = recording["fecha_transcripcion"].isoformat()
    
    return recordings

@router.get("/{recording_id}/download")
async def download_audio(
    recording_id: str,
    mongo_db = Depends(get_mongo_db)
):
    """Download audio recording"""
    
    try:
        from bson import ObjectId
        recording = mongo_db.audio_registros.find_one({"_id": ObjectId(recording_id)})
        
        if not recording:
            raise HTTPException(status_code=404, detail="Audio recording not found")
        
        file_path = recording["archivo_path"]
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        from fastapi.responses import FileResponse
        return FileResponse(
            path=file_path,
            filename=f"recording_{recording_id}.{recording['formato']}",
            media_type=f"audio/{recording['formato']}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download audio: {str(e)}")

@router.post("/{recording_id}/transcribe")
async def transcribe_audio(
    recording_id: str,
    mongo_db = Depends(get_mongo_db)
):
    """Transcribe audio recording (placeholder for speech-to-text integration)"""
    
    try:
        from bson import ObjectId
        recording = mongo_db.audio_registros.find_one({"_id": ObjectId(recording_id)})
        
        if not recording:
            raise HTTPException(status_code=404, detail="Audio recording not found")
        
        # Update status to processing
        mongo_db.audio_registros.update_one(
            {"_id": ObjectId(recording_id)},
            {"$set": {"estado": "procesando"}}
        )
        
        # TODO: Implement actual speech-to-text service
        # For now, we'll add a placeholder transcription
        placeholder_transcription = "Transcripción no disponible - servicio de voz a texto no configurado"
        
        # Update with transcription
        mongo_db.audio_registros.update_one(
            {"_id": ObjectId(recording_id)},
            {
                "$set": {
                    "transcripcion": placeholder_transcription,
                    "fecha_transcripcion": datetime.utcnow(),
                    "estado": "transcrito"
                }
            }
        )
        
        return {
            "message": "Audio transcribed successfully",
            "transcription": placeholder_transcription
        }
    except Exception as e:
        # Update status to error
        mongo_db.audio_registros.update_one(
            {"_id": ObjectId(recording_id)},
            {"$set": {"estado": "error"}}
        )
        raise HTTPException(status_code=500, detail=f"Failed to transcribe audio: {str(e)}")

@router.delete("/{recording_id}")
async def delete_audio(
    recording_id: str,
    mongo_db = Depends(get_mongo_db)
):
    """Delete audio recording"""
    
    try:
        from bson import ObjectId
        recording = mongo_db.audio_registros.find_one({"_id": ObjectId(recording_id)})
        
        if not recording:
            raise HTTPException(status_code=404, detail="Audio recording not found")
        
        # Delete file from filesystem
        file_path = recording["archivo_path"]
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete from MongoDB
        mongo_db.audio_registros.delete_one({"_id": ObjectId(recording_id)})
        
        return {"message": "Audio recording deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete audio: {str(e)}")
