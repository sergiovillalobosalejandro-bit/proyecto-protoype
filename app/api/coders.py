from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models import Coder, Clan
from ..schemas import CoderCreate, CoderResponse, CoderUpdate, CoderWithDetails, CoderSimpleResponse

router = APIRouter()

@router.get("/", response_model=List[CoderSimpleResponse])
async def get_coders(db: Session = Depends(get_db)):
    """Get all coders"""
    coders = db.query(Coder).all()
    return coders

@router.get("/{coder_id}", response_model=CoderWithDetails)
async def get_coder(coder_id: int, db: Session = Depends(get_db)):
    """Get coder by ID"""
    coder = db.query(Coder).filter(Coder.id_coder == coder_id).first()
    if not coder:
        raise HTTPException(status_code=404, detail="Coder not found")
    return coder

@router.get("/search/{document_id}", response_model=CoderWithDetails)
async def search_coder_by_document(document_id: str, db: Session = Depends(get_db)):
    """Search coder by document ID"""
    coder = db.query(Coder).filter(Coder.document_id == document_id).first()
    if not coder:
        raise HTTPException(status_code=404, detail="Coder not found")
    return coder

@router.post("/", response_model=CoderResponse, status_code=status.HTTP_201_CREATED)
async def create_coder(coder: CoderCreate, db: Session = Depends(get_db)):
    """Create new coder"""
    # Verify clan exists
    clan = db.query(Clan).filter(Clan.id_clan == coder.id_clan).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    
    db_coder = Coder(**coder.model_dump())
    db.add(db_coder)
    db.commit()
    db.refresh(db_coder)
    return db_coder

@router.put("/{coder_id}", response_model=CoderResponse)
async def update_coder(coder_id: int, coder: CoderUpdate, db: Session = Depends(get_db)):
    """Update coder"""
    db_coder = db.query(Coder).filter(Coder.id_coder == coder_id).first()
    if not db_coder:
        raise HTTPException(status_code=404, detail="Coder not found")
    
    update_data = coder.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_coder, field, value)
    
    db.commit()
    db.refresh(db_coder)
    return db_coder

@router.delete("/{coder_id}")
async def delete_coder(coder_id: int, db: Session = Depends(get_db)):
    """Delete coder"""
    db_coder = db.query(Coder).filter(Coder.id_coder == coder_id).first()
    if not db_coder:
        raise HTTPException(status_code=404, detail="Coder not found")
    
    db.delete(db_coder)
    db.commit()
    return {"message": "Coder deleted successfully"}

@router.get("/clan/{clan_id}", response_model=List[CoderResponse])
async def get_coders_by_clan(clan_id: int, db: Session = Depends(get_db)):
    """Get coders by clan"""
    coders = db.query(Coder).filter(Coder.id_clan == clan_id).all()
    return coders
