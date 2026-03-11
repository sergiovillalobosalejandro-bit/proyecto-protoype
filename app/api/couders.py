from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..core.database import get_db
from ..models import Couder, Clan, Corte, Sede, EstadoCouder
from ..schemas.couders import CouderResponse, CouderCreate, CouderUpdate, CouderWithDetails

router = APIRouter()

@router.get("/search/{cc}", response_model=CouderWithDetails)
async def search_couder_by_cc(cc: str, db: Session = Depends(get_db)):
    couder = db.query(Couder).filter(Couder.cc == cc, Couder.activo == True).first()
    if not couder:
        raise HTTPException(status_code=404, detail="Couder not found")
    
    # Get clan, corte, and sede information
    clan = db.query(Clan).filter(Clan.id == couder.clan_id).first()
    corte = db.query(Corte).filter(Corte.id == clan.corte_id).first() if clan else None
    sede = db.query(Sede).filter(Sede.id == corte.sede_id).first() if corte else None
    
    return CouderWithDetails(
        id=couder.id,
        cc=couder.cc,
        nombre_completo=couder.nombre_completo,
        fecha_nacimiento=couder.fecha_nacimiento,
        telefono=couder.telefono,
        email=couder.email,
        direccion=couder.direccion,
        estado=couder.estado,
        fecha_ingreso=couder.fecha_ingreso,
        fecha_retiro=couder.fecha_retiro,
        fecha_completado=couder.fecha_completado,
        clan=clan,
        corte=corte,
        sede=sede
    )

@router.get("/", response_model=List[CouderResponse])
async def get_couders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    clan_id: Optional[int] = Query(None),
    estado: Optional[EstadoCouder] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Couder).filter(Couder.activo == True)
    
    if clan_id:
        query = query.filter(Couder.clan_id == clan_id)
    
    if estado:
        query = query.filter(Couder.estado == estado)
    
    couders = query.offset(skip).limit(limit).all()
    return couders

@router.post("/", response_model=CouderResponse)
async def create_couder(couder: CouderCreate, db: Session = Depends(get_db)):
    # Check if CC already exists
    existing_couder = db.query(Couder).filter(Couder.cc == couder.cc).first()
    if existing_couder:
        raise HTTPException(status_code=400, detail="CC already exists")
    
    # Verify clan exists
    clan = db.query(Clan).filter(Clan.id == couder.clan_id, Clan.activo == True).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    
    db_couder = Couder(**couder.dict())
    db.add(db_couder)
    db.commit()
    db.refresh(db_couder)
    
    return db_couder

@router.put("/{couder_id}", response_model=CouderResponse)
async def update_couder(
    couder_id: int, 
    couder_update: CouderUpdate, 
    db: Session = Depends(get_db)
):
    couder = db.query(Couder).filter(Couder.id == couder_id, Couder.activo == True).first()
    if not couder:
        raise HTTPException(status_code=404, detail="Couder not found")
    
    update_data = couder_update.dict(exclude_unset=True)
    
    # Handle state changes with timestamps
    if "estado" in update_data:
        new_state = update_data["estado"]
        if new_state == EstadoCouder.RETIRADO and not couder.fecha_retiro:
            update_data["fecha_retiro"] = datetime.utcnow()
        elif new_state == EstadoCouder.COMPLETADO and not couder.fecha_completado:
            update_data["fecha_completado"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(couder, field, value)
    
    db.commit()
    db.refresh(couder)
    
    return couder

@router.delete("/{couder_id}")
async def delete_couder(couder_id: int, db: Session = Depends(get_db)):
    couder = db.query(Couder).filter(Couder.id == couder_id).first()
    if not couder:
        raise HTTPException(status_code=404, detail="Couder not found")
    
    couder.activo = False
    db.commit()
    
    return {"message": "Couder deleted successfully"}

@router.get("/clan/{clan_id}", response_model=List[CouderResponse])
async def get_couders_by_clan(clan_id: int, db: Session = Depends(get_db)):
    couders = db.query(Couder).filter(
        Couder.clan_id == clan_id, 
        Couder.activo == True
    ).all()
    return couders
