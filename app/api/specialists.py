from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import Specialist
from ..schemas import SpecialistCreate, SpecialistResponse, SpecialistUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@router.get("/", response_model=List[SpecialistResponse])
async def get_specialists(db: Session = Depends(get_db)):
    """Get all specialists (without passwords)"""
    specialists = db.query(Specialist).all()
    return specialists

@router.get("/{specialist_id}", response_model=SpecialistResponse)
async def get_specialist(specialist_id: int, db: Session = Depends(get_db)):
    """Get specialist by ID (without password)"""
    specialist = db.query(Specialist).filter(Specialist.id_specialist == specialist_id).first()
    if not specialist:
        raise HTTPException(status_code=404, detail="Specialist not found")
    return specialist

@router.post("/", response_model=SpecialistResponse, status_code=status.HTTP_201_CREATED)
async def create_specialist(specialist: SpecialistCreate, db: Session = Depends(get_db)):
    """Create new specialist"""
    # Hash password
    specialist_data = specialist.model_dump()
    specialist_data['password'] = get_password_hash(specialist_data['password'])
    
    db_specialist = Specialist(**specialist_data)
    db.add(db_specialist)
    db.commit()
    db.refresh(db_specialist)
    return db_specialist

@router.put("/{specialist_id}", response_model=SpecialistResponse)
async def update_specialist(specialist_id: int, specialist: SpecialistUpdate, db: Session = Depends(get_db)):
    """Update specialist"""
    db_specialist = db.query(Specialist).filter(Specialist.id_specialist == specialist_id).first()
    if not db_specialist:
        raise HTTPException(status_code=404, detail="Specialist not found")
    
    update_data = specialist.model_dump(exclude_unset=True)
    
    # Hash password if provided
    if 'password' in update_data and update_data['password']:
        update_data['password'] = get_password_hash(update_data['password'])
    
    for field, value in update_data.items():
        setattr(db_specialist, field, value)
    
    db.commit()
    db.refresh(db_specialist)
    return db_specialist

@router.delete("/{specialist_id}")
async def delete_specialist(specialist_id: int, db: Session = Depends(get_db)):
    """Delete specialist"""
    db_specialist = db.query(Specialist).filter(Specialist.id_specialist == specialist_id).first()
    if not db_specialist:
        raise HTTPException(status_code=404, detail="Specialist not found")
    
    db.delete(db_specialist)
    db.commit()
    return {"message": "Specialist deleted successfully"}
