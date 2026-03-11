from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..core.database import get_db
from ..core.mongodb import get_mongo_db
from ..services.ai_service import ai_service
from ..models import Couder, Intervencion

router = APIRouter()

@router.post("/synthesize/{couder_id}")
async def synthesize_interventions(
    couder_id: int,
    intervention_ids: List[int],
    db: Session = Depends(get_db)
):
    """Generate AI synthesis of interventions for a couder"""
    
    # Verify couder exists
    couder = db.query(Couder).filter(Couder.id == couder_id, Couder.activo == True).first()
    if not couder:
        raise HTTPException(status_code=404, detail="Couder not found")
    
    # Verify interventions exist and belong to the couder
    interventions = db.query(Intervencion).filter(
        Intervencion.id.in_(intervention_ids),
        Intervencion.couder_id == couder_id
    ).all()
    
    if len(interventions) != len(intervention_ids):
        raise HTTPException(status_code=400, detail="Some interventions not found or don't belong to this couder")
    
    try:
        synthesis = await ai_service.synthesize_interventions(couder_id, intervention_ids)
        return synthesis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI synthesis failed: {str(e)}")

@router.post("/diagnose/{couder_id}")
async def generate_diagnosis(
    couder_id: int,
    intervention_ids: List[int],
    db: Session = Depends(get_db)
):
    """Generate mini-diagnosis based on interventions"""
    
    # Verify couder exists
    couder = db.query(Couder).filter(Couder.id == couder_id, Couder.activo == True).first()
    if not couder:
        raise HTTPException(status_code=404, detail="Couder not found")
    
    # Verify interventions exist and belong to the couder
    interventions = db.query(Intervencion).filter(
        Intervencion.id.in_(intervention_ids),
        Intervencion.couder_id == couder_id
    ).all()
    
    if len(interventions) != len(intervention_ids):
        raise HTTPException(status_code=400, detail="Some interventions not found or don't belong to this couder")
    
    try:
        diagnosis = await ai_service.generate_diagnosis(couder_id, intervention_ids)
        return diagnosis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI diagnosis failed: {str(e)}")

@router.get("/analyses/{couder_id}")
async def get_historical_analyses(
    couder_id: int,
    analysis_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get historical AI analyses for a couder"""
    
    # Verify couder exists
    couder = db.query(Couder).filter(Couder.id == couder_id, Couder.activo == True).first()
    if not couder:
        raise HTTPException(status_code=404, detail="Couder not found")
    
    try:
        analyses = await ai_service.get_historical_analyses(couder_id, analysis_type)
        return analyses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analyses: {str(e)}")

@router.get("/analysis/{analysis_id}")
async def get_specific_analysis(
    analysis_id: str,
    mongo_db = Depends(get_mongo_db)
):
    """Get a specific AI analysis by ID"""
    
    try:
        from bson import ObjectId
        analysis = mongo_db.ai_analisis.find_one({"_id": ObjectId(analysis_id)})
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        # Convert ObjectId to string
        analysis["_id"] = str(analysis["_id"])
        if "fecha_generacion" in analysis:
            analysis["fecha_generacion"] = analysis["fecha_generacion"].isoformat()
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analysis: {str(e)}")

@router.delete("/analysis/{analysis_id}")
async def delete_analysis(
    analysis_id: str,
    mongo_db = Depends(get_mongo_db)
):
    """Delete an AI analysis"""
    
    try:
        from bson import ObjectId
        result = mongo_db.ai_analisis.delete_one({"_id": ObjectId(analysis_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return {"message": "Analysis deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete analysis: {str(e)}")
