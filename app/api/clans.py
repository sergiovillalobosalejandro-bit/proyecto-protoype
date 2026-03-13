from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models import Clan, Cohort
from ..schemas import ClanCreate, ClanResponse, ClanUpdate

router = APIRouter()

@router.get("/", response_model=List[ClanResponse])
async def get_clans(db: Session = Depends(get_db)):
    """Get all clans"""
    clans = db.query(Clan).all()
    return clans

@router.get("/{clan_id}", response_model=ClanResponse)
async def get_clan(clan_id: int, db: Session = Depends(get_db)):
    """Get clan by ID"""
    clan = db.query(Clan).filter(Clan.id_clan == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    return clan

@router.post("/", response_model=ClanResponse)
async def create_clan(clan: ClanCreate, db: Session = Depends(get_db)):
    """Create a new clan"""
    # Verify cohort exists
    cohort = db.query(Cohort).filter(Cohort.id_cohort == clan.id_cohort).first()
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    db_clan = Clan(**clan.dict())
    db.add(db_clan)
    db.commit()
    db.refresh(db_clan)
    return db_clan

@router.put("/{clan_id}", response_model=ClanResponse)
async def update_clan(clan_id: int, clan: ClanUpdate, db: Session = Depends(get_db)):
    """Update clan"""
    db_clan = db.query(Clan).filter(Clan.id_clan == clan_id).first()
    if not db_clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    
    for key, value in clan.dict(exclude_unset=True).items():
        setattr(db_clan, key, value)
    
    db.commit()
    db.refresh(db_clan)
    return db_clan

@router.delete("/{clan_id}")
async def delete_clan(clan_id: int, db: Session = Depends(get_db)):
    """Delete clan"""
    db_clan = db.query(Clan).filter(Clan.id_clan == clan_id).first()
    if not db_clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    
    db.delete(db_clan)
    db.commit()
    return {"message": "Clan deleted successfully"}

@router.get("/cohort/{cohort_id}", response_model=List[ClanResponse])
async def get_clans_by_cohort(cohort_id: int, db: Session = Depends(get_db)):
    """Get all clans for a specific cohort"""
    clans = db.query(Clan).filter(Clan.id_cohort == cohort_id).all()
    return clans
