from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from ..core.database import get_db
from ..models import Sede, Corte, Clan, Couder, EstadoCouder, TipoRuta, Jornada

router = APIRouter()

@router.get("/overview")
async def get_dashboard_overview(db: Session = Depends(get_db)):
    """Get main dashboard metrics - Optimized with single query"""
    
    # Single optimized query for all metrics
    metrics_query = db.query(
        Sede.id.label('sede_id'),
        Sede.nombre.label('sede_nombre'),
        Corte.id.label('corte_id'),
        Corte.nombre.label('corte_nombre'),
        Clan.id.label('clan_id'),
        Clan.nombre.label('clan_nombre'),
        Clan.jornada.label('clan_jornada'),
        Corte.tipo_ruta.label('corte_tipo_ruta'),
        func.count(Couder.id).label('total_couders'),
        func.sum(func.case([(Couder.estado == EstadoCouder.ACTIVO, 1)], else_=0)).label('activos'),
        func.sum(func.case([(Couder.estado == EstadoCouder.RETIRADO, 1)], else_=0)).label('retirados'),
        func.sum(func.case([(Couder.estado == EstadoCouder.COMPLETADO, 1)], else_=0)).label('completados')
    ).join(Corte, Sede.id == Corte.sede_id)\
     .join(Clan, Corte.id == Clan.corte_id)\
     .join(Couder, Clan.id == Couder.clan_id)\
     .filter(Couder.activo == True)\
     .group_by(Sede.id, Sede.nombre, Corte.id, Corte.nombre, Clan.id, Clan.nombre, Clan.jornada, Corte.tipo_ruta)
    
    results = metrics_query.all()
    
    # Calculate totals from results
    total_couders = sum(r.total_couders or 0 for r in results)
    activos_couders = sum(r.activos or 0 for r in results)
    retirados_couders = sum(r.retirados or 0 for r in results)
    completados_couders = sum(r.completados or 0 for r in results)
    
    # Group by sede
    sedes_dict = {}
    for r in results:
        if r.sede_id not in sedes_dict:
            sedes_dict[r.sede_id] = {
                "id": r.sede_id,
                "nombre": r.sede_nombre,
                "total_couders": 0,
                "activos": 0,
                "retirados": 0,
                "completados": 0,
                "intervention_percentage": 0,
                "cortes": {}
            }
        
        sede_data = sedes_dict[r.sede_id]
        sede_data["total_couders"] += r.total_couders or 0
        sede_data["activos"] += r.activos or 0
        sede_data["retirados"] += r.retirados or 0
        sede_data["completados"] += r.completados or 0
        
        # Group by corte within sede
        if r.corte_id not in sede_data["cortes"]:
            sede_data["cortes"][r.corte_id] = {
                "id": r.corte_id,
                "nombre": r.corte_nombre,
                "tipo_ruta": r.corte_tipo_ruta.value,
                "total_couders": 0,
                "activos": 0,
                "retirados": 0,
                "completados": 0,
                "intervention_percentage": 0,
                "clanes": {}
            }
        
        corte_data = sede_data["cortes"][r.corte_id]
        corte_data["total_couders"] += r.total_couders or 0
        corte_data["activos"] += r.activos or 0
        corte_data["retirados"] += r.retirados or 0
        corte_data["completados"] += r.completados or 0
        
        # Add clan data
        corte_data["clanes"][r.clan_id] = {
            "id": r.clan_id,
            "nombre": r.clan_nombre,
            "jornada": r.clan_jornada.value,
            "total_couders": r.total_couders or 0,
            "activos": r.activos or 0,
            "retirados": r.retirados or 0,
            "completados": r.completados or 0,
            "intervention_percentage": (r.activos or 0) / (r.total_couders or 1) * 100
        }
    
    # Calculate percentages and format response
    sedes_metrics = []
    for sede_data in sedes_dict.values():
        total = sede_data["total_couders"]
        intervention_percentage = sede_data["activos"] / total * 100 if total > 0 else 0
        sede_data["intervention_percentage"] = intervention_percentage
        
        # Calculate corte percentages
        for corte_data in sede_data["cortes"].values():
            total = corte_data["total_couders"]
            intervention_percentage = corte_data["activos"] / total * 100 if total > 0 else 0
            corte_data["intervention_percentage"] = intervention_percentage
            corte_data["clanes"] = list(corte_data["clanes"].values())
        
        sede_data["cortes"] = list(sede_data["cortes"].values())
        sedes_metrics.append(sede_data)
    
    return {
        "total_metrics": {
            "total_couders": total_couders,
            "activos": activos_couders,
            "retirados": retirados_couders,
            "completados": completados_couders
        },
        "sedes": sedes_metrics
    }

@router.get("/sedes/{sede_id}")
async def get_sede_details(sede_id: int, db: Session = Depends(get_db)):
    """Get detailed metrics for a specific sede"""
    
    # Verify sede exists
    sede = db.query(Sede).filter(Sede.id == sede_id, Sede.activa == True).first()
    if not sede:
        raise HTTPException(status_code=404, detail="Sede not found")
    
    # Get cortes for this sede
    cortes_query = db.query(
        Corte.id,
        Corte.nombre,
        Corte.tipo_ruta,
        Corte.fecha_inicio,
        Corte.fecha_fin,
        func.count(Couder.id).label('total_couders'),
        func.sum(func.case([(Couder.estado == EstadoCouder.ACTIVO, 1)], else_=0)).label('activos'),
        func.sum(func.case([(Couder.estado == EstadoCouder.RETIRADO, 1)], else_=0)).label('retirados'),
        func.sum(func.case([(Couder.estado == EstadoCouder.COMPLETADO, 1)], else_=0)).label('completados')
    ).join(Clan, Corte.id == Clan.corte_id)\
     .join(Couder, Clan.id == Couder.clan_id)\
     .filter(Corte.sede_id == sede_id, Couder.activo == True)\
     .group_by(Corte.id)\
     .all()
    
    cortes_metrics = []
    for corte in cortes_query:
        total = corte.total_couders or 0
        intervention_percentage = (corte.activos or 0) / total * 100 if total > 0 else 0
        
        cortes_metrics.append({
            "id": corte.id,
            "nombre": corte.nombre,
            "tipo_ruta": corte.tipo_ruta.value,
            "fecha_inicio": corte.fecha_inicio,
            "fecha_fin": corte.fecha_fin,
            "total_couders": total,
            "activos": corte.activos or 0,
            "retirados": corte.retirados or 0,
            "completados": corte.completados or 0,
            "porcentaje_atendidos": round(intervention_percentage, 2)
        })
    
    return {
        "sede": {
            "id": sede.id,
            "nombre": sede.nombre,
            "direccion": sede.direccion,
            "telefono": sede.telefono,
            "email": sede.email
        },
        "cortes": cortes_metrics
    }

@router.get("/cortes/{corte_id}")
async def get_corte_details(corte_id: int, db: Session = Depends(get_db)):
    """Get detailed metrics for a specific corte"""
    
    # Verify corte exists
    corte = db.query(Corte).filter(Corte.id == corte_id, Corte.activo == True).first()
    if not corte:
        raise HTTPException(status_code=404, detail="Corte not found")
    
    # Get clanes for this corte, organized by jornada
    clanes_am = db.query(
        Clan.id,
        Clan.nombre,
        Clan.capacidad_maxima,
        func.count(Couder.id).label('total_couders'),
        func.sum(func.case([(Couder.estado == EstadoCouder.ACTIVO, 1)], else_=0)).label('activos'),
        func.sum(func.case([(Couder.estado == EstadoCouder.RETIRADO, 1)], else_=0)).label('retirados'),
        func.sum(func.case([(Couder.estado == EstadoCouder.COMPLETADO, 1)], else_=0)).label('completados')
    ).join(Couder, Clan.id == Couder.clan_id)\
     .filter(Clan.corte_id == corte_id, Clan.jornada == Jornada.AM, Clan.activo == True, Couder.activo == True)\
     .group_by(Clan.id)\
     .all()
    
    clanes_pm = db.query(
        Clan.id,
        Clan.nombre,
        Clan.capacidad_maxima,
        func.count(Couder.id).label('total_couders'),
        func.sum(func.case([(Couder.estado == EstadoCouder.ACTIVO, 1)], else_=0)).label('activos'),
        func.sum(func.case([(Couder.estado == EstadoCouder.RETIRADO, 1)], else_=0)).label('retirados'),
        func.sum(func.case([(Couder.estado == EstadoCouder.COMPLETADO, 1)], else_=0)).label('completados')
    ).join(Couder, Clan.id == Couder.clan_id)\
     .filter(Clan.corte_id == corte_id, Clan.jornada == Jornada.PM, Clan.activo == True, Couder.activo == True)\
     .group_by(Clan.id)\
     .all()
    
    def format_clan(clan):
        total = clan.total_couders or 0
        return {
            "id": clan.id,
            "nombre": clan.nombre,
            "capacidad_maxima": clan.capacidad_maxima,
            "total_couders": total,
            "activos": clan.activos or 0,
            "retirados": clan.retirados or 0,
            "completados": clan.completados or 0
        }
    
    return {
        "corte": {
            "id": corte.id,
            "nombre": corte.nombre,
            "tipo_ruta": corte.tipo_ruta.value,
            "fecha_inicio": corte.fecha_inicio,
            "fecha_fin": corte.fecha_fin
        },
        "clanes_am": [format_clan(clan) for clan in clanes_am],
        "clanes_pm": [format_clan(clan) for clan in clanes_pm]
    }

@router.get("/clanes/{clan_id}")
async def get_clan_details(clan_id: int, db: Session = Depends(get_db)):
    """Get detailed metrics for a specific clan"""
    
    # Verify clan exists
    clan = db.query(Clan).filter(Clan.id == clan_id, Clan.activo == True).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    
    # Get couders for this clan
    couders_count = db.query(Couder).filter(
        Couder.clan_id == clan_id, 
        Couder.activo == True
    ).count()
    
    activos_count = db.query(Couder).filter(
        Couder.clan_id == clan_id, 
        Couder.estado == EstadoCouder.ACTIVO,
        Couder.activo == True
    ).count()
    
    retirados_count = db.query(Couder).filter(
        Couder.clan_id == clan_id, 
        Couder.estado == EstadoCouder.RETIRADO,
        Couder.activo == True
    ).count()
    
    completados_count = db.query(Couder).filter(
        Couder.clan_id == clan_id, 
        Couder.estado == EstadoCouder.COMPLETADO,
        Couder.activo == True
    ).count()
    
    return {
        "clan": {
            "id": clan.id,
            "nombre": clan.nombre,
            "jornada": clan.jornada.value,
            "capacidad_maxima": clan.capacidad_maxima
        },
        "metricas": {
            "total_couders": couders_count,
            "activos": activos_count,
            "retirados": retirados_count,
            "completados": completados_count
        }
    }
