from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import Campus
from ..schemas import CampusCreate, CampusResponse, CampusUpdate

router = APIRouter()

@router.get("/", response_model=List[CampusResponse])
async def get_campuses(db: Session = Depends(get_db)):
    """Get all campuses"""
    campuses = db.query(Campus).all()
    return campuses

@router.get("/{campus_id}", response_model=CampusResponse)
async def get_campus(campus_id: int, db: Session = Depends(get_db)):
    """Get campus by ID"""
    campus = db.query(Campus).filter(Campus.id_campus == campus_id).first()
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    return campus

@router.post("/", response_model=CampusResponse, status_code=status.HTTP_201_CREATED)
async def create_campus(campus: CampusCreate, db: Session = Depends(get_db)):
    """Create new campus"""
    db_campus = Campus(**campus.model_dump())
    db.add(db_campus)
    db.commit()
    db.refresh(db_campus)
    return db_campus

@router.put("/{campus_id}", response_model=CampusResponse)
async def update_campus(campus_id: int, campus: CampusUpdate, db: Session = Depends(get_db)):
    """Update campus"""
    db_campus = db.query(Campus).filter(Campus.id_campus == campus_id).first()
    if not db_campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    update_data = campus.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_campus, field, value)
    
    db.commit()
    db.refresh(db_campus)
    return db_campus

@router.delete("/{campus_id}")
async def delete_campus(campus_id: int, db: Session = Depends(get_db)):
    """Delete campus"""
    db_campus = db.query(Campus).filter(Campus.id_campus == campus_id).first()
    if not db_campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    db.delete(db_campus)
    db.commit()
    return {"message": "Campus deleted successfully"}
