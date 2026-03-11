from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..core.database import get_db
from ..core.mongodb import get_mongo_db
from ..models import Intervencion, Couder, Usuario
from ..schemas.intervenciones import IntervencionResponse, IntervencionCreate, IntervencionUpdate, ClinicalHistoryRecord

router = APIRouter()

@router.get("/couder/{couder_id}", response_model=List[IntervencionResponse])
async def get_intervenciones_by_couder(
    couder_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    # Verify couder exists
    couder = db.query(Couder).filter(Couder.id == couder_id, Couder.activo == True).first()
    if not couder:
        raise HTTPException(status_code=404, detail="Couder not found")
    
    intervenciones = db.query(Intervencion).filter(
        Intervencion.couder_id == couder_id
    ).order_by(Intervencion.fecha_intervencion.desc()).offset(skip).limit(limit).all()
    
    return intervenciones

@router.post("/", response_model=IntervencionResponse)
async def create_intervencion(
    intervencion: IntervencionCreate,
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    # Verify couder exists
    couder = db.query(Couder).filter(Couder.id == intervencion.couder_id, Couder.activo == True).first()
    if not couder:
        raise HTTPException(status_code=404, detail="Couder not found")
    
    # Verify user exists
    usuario = db.query(Usuario).filter(Usuario.id == intervencion.usuario_id, Usuario.activo == True).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_intervencion = Intervencion(**intervencion.dict())
    db.add(db_intervencion)
    db.commit()
    db.refresh(db_intervencion)
    
    # Create clinical history record in MongoDB
    clinical_record = {
        "couder_id": intervencion.couder_id,
        "intervencion_id": db_intervencion.id,
        "notas_completas": intervencion.descripcion,
        "sintomas_observados": [],
        "estado_emocional": "No especificado",
        "nivel_participacion": "No evaluado",
        "observaciones_adicionales": intervencion.observaciones or "",
        "fecha_registro": datetime.utcnow(),
        "actualizado_en": datetime.utcnow()
    }
    
    mongo_db.historial_clinico.insert_one(clinical_record)
    
    return db_intervencion

@router.put("/{intervencion_id}", response_model=IntervencionResponse)
async def update_intervencion(
    intervencion_id: int,
    intervencion_update: IntervencionUpdate,
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    intervencion = db.query(Intervencion).filter(Intervencion.id == intervencion_id).first()
    if not intervencion:
        raise HTTPException(status_code=404, detail="Intervencion not found")
    
    update_data = intervencion_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(intervencion, field, value)
    
    db.commit()
    db.refresh(intervencion)
    
    # Update MongoDB record
    if "descripcion" in update_data or "observaciones" in update_data:
        mongo_db.historial_clinico.update_one(
            {"intervencion_id": intervencion_id},
            {
                "$set": {
                    "notas_completas": intervencion.descripcion,
                    "observaciones_adicionales": intervencion.observaciones or "",
                    "actualizado_en": datetime.utcnow()
                }
            }
        )
    
    return intervencion

@router.delete("/{intervencion_id}")
async def delete_intervencion(
    intervencion_id: int,
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    intervencion = db.query(Intervencion).filter(Intervencion.id == intervencion_id).first()
    if not intervencion:
        raise HTTPException(status_code=404, detail="Intervencion not found")
    
    db.delete(intervencion)
    db.commit()
    
    # Delete from MongoDB
    mongo_db.historial_clinico.delete_one({"intervencion_id": intervencion_id})
    
    return {"message": "Intervencion deleted successfully"}

@router.get("/clinical-history/{couder_id}", response_model=List[ClinicalHistoryRecord])
async def get_clinical_history(
    couder_id: int,
    limit: int = Query(50, ge=1, le=200),
    mongo_db = Depends(get_mongo_db)
):
    # Verify couder exists
    couder = db.query(Couder).filter(Couder.id == couder_id, Couder.activo == True).first()
    if not couder:
        raise HTTPException(status_code=404, detail="Couder not found")
    
    # Get clinical history from MongoDB
    records = list(mongo_db.historial_clinico.find(
        {"couder_id": couder_id}
    ).sort("fecha_registro", -1).limit(limit))
    
    # Convert ObjectId to string for JSON serialization
    for record in records:
        if "_id" in record:
            record["_id"] = str(record["_id"])
    
    return records
