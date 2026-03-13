from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models import History, Coder, Specialist
from ..schemas import HistoryCreate, HistoryResponse, HistoryUpdate

router = APIRouter()

@router.get("/", response_model=List[HistoryResponse])
async def get_histories(db: Session = Depends(get_db)):
    """Get all histories"""
    histories = db.query(History).all()
    return histories

@router.get("/{history_id}", response_model=HistoryResponse)
async def get_history(history_id: int, db: Session = Depends(get_db)):
    """Get history by ID"""
    history = db.query(History).filter(History.id_history == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    return history

@router.get("/coder/{coder_id}", response_model=List[HistoryResponse])
async def get_histories_by_coder(coder_id: int, db: Session = Depends(get_db)):
    """Get histories by coder"""
    # Verify coder exists
    coder = db.query(Coder).filter(Coder.id_coder == coder_id).first()
    if not coder:
        raise HTTPException(status_code=404, detail="Coder not found")
    
    histories = db.query(History).filter(History.id_coder == coder_id).order_by(History.date_time.desc()).all()
    return histories

@router.get("/specialist/{specialist_id}", response_model=List[HistoryResponse])
async def get_histories_by_specialist(specialist_id: int, db: Session = Depends(get_db)):
    """Get histories by specialist"""
    # Verify specialist exists
    specialist = db.query(Specialist).filter(Specialist.id_specialist == specialist_id).first()
    if not specialist:
        raise HTTPException(status_code=404, detail="Specialist not found")
    
    histories = db.query(History).filter(History.id_specialist == specialist_id).order_by(History.date_time.desc()).all()
    return histories

@router.post("/", response_model=HistoryResponse, status_code=status.HTTP_201_CREATED)
async def create_history(history: HistoryCreate, db: Session = Depends(get_db)):
    """Create new history"""
    # Verify coder exists
    coder = db.query(Coder).filter(Coder.id_coder == history.id_coder).first()
    if not coder:
        raise HTTPException(status_code=404, detail="Coder not found")
    
    # Verify specialist exists
    specialist = db.query(Specialist).filter(Specialist.id_specialist == history.id_specialist).first()
    if not specialist:
        raise HTTPException(status_code=404, detail="Specialist not found")
    
    db_history = History(**history.model_dump())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

@router.put("/{history_id}", response_model=HistoryResponse)
async def update_history(history_id: int, history: HistoryUpdate, db: Session = Depends(get_db)):
    """Update history"""
    db_history = db.query(History).filter(History.id_history == history_id).first()
    if not db_history:
        raise HTTPException(status_code=404, detail="History not found")
    
    update_data = history.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_history, field, value)
    
    db.commit()
    db.refresh(db_history)
    return db_history

@router.delete("/{history_id}")
async def delete_history(history_id: int, db: Session = Depends(get_db)):
    """Delete history"""
    db_history = db.query(History).filter(History.id_history == history_id).first()
    if not db_history:
        raise HTTPException(status_code=404, detail="History not found")
    
    db.delete(db_history)
    db.commit()
    return {"message": "History deleted successfully"}
