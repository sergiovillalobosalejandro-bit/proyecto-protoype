from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models import Cohort, Campus
from ..schemas import CohortCreate, CohortResponse, CohortUpdate

router = APIRouter()

@router.get("/", response_model=List[CohortResponse])
async def get_cohorts(db: Session = Depends(get_db)):
    """Get all cohorts"""
    cohorts = db.query(Cohort).all()
    return cohorts

@router.get("/{cohort_id}", response_model=CohortResponse)
async def get_cohort(cohort_id: int, db: Session = Depends(get_db)):
    """Get cohort by ID"""
    cohort = db.query(Cohort).filter(Cohort.id_cohort == cohort_id).first()
    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    return cohort

@router.post("/", response_model=CohortResponse, status_code=status.HTTP_201_CREATED)
async def create_cohort(cohort: CohortCreate, db: Session = Depends(get_db)):
    """Create new cohort"""
    # Verify campus exists
    campus = db.query(Campus).filter(Campus.id_campus == cohort.id_campus).first()
    if not campus:
        raise HTTPException(status_code=404, detail="Campus not found")
    
    db_cohort = Cohort(**cohort.model_dump())
    db.add(db_cohort)
    db.commit()
    db.refresh(db_cohort)
    return db_cohort

@router.put("/{cohort_id}", response_model=CohortResponse)
async def update_cohort(cohort_id: int, cohort: CohortUpdate, db: Session = Depends(get_db)):
    """Update cohort"""
    db_cohort = db.query(Cohort).filter(Cohort.id_cohort == cohort_id).first()
    if not db_cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    update_data = cohort.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_cohort, field, value)
    
    db.commit()
    db.refresh(db_cohort)
    return db_cohort

@router.delete("/{cohort_id}")
async def delete_cohort(cohort_id: int, db: Session = Depends(get_db)):
    """Delete cohort"""
    db_cohort = db.query(Cohort).filter(Cohort.id_cohort == cohort_id).first()
    if not db_cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")
    
    db.delete(db_cohort)
    db.commit()
    return {"message": "Cohort deleted successfully"}

@router.get("/campus/{campus_id}", response_model=List[CohortResponse])
async def get_cohorts_by_campus(campus_id: int, db: Session = Depends(get_db)):
    """Get cohorts by campus"""
    cohorts = db.query(Cohort).filter(Cohort.id_campus == campus_id).all()
    return cohorts
