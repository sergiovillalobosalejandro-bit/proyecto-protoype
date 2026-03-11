from typing import Dict, List, Any, Optional
from datetime import datetime
from openai import OpenAI
from ..core.config import settings
from ..core.mongodb import get_mongo_db

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
    
    async def synthesize_interventions(self, couder_id: int, intervention_ids: List[int]) -> Dict[str, Any]:
        """Generate AI synthesis of interventions for a couder"""
        if not self.client:
            raise Exception("OpenAI API key not configured")
        
        mongo_db = get_mongo_db()
        
        # Get clinical records for the interventions
        records = list(mongo_db.historial_clinico.find({
            "couder_id": couder_id,
            "intervencion_id": {"$in": intervention_ids}
        }).sort("fecha_registro", 1))
        
        if not records:
            raise Exception("No clinical records found for synthesis")
        
        # Prepare context for AI
        context = self._prepare_synthesis_context(records)
        
        # Generate synthesis using OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """Eres un psicólogo clínico especializado en intervención con jóvenes. 
                    Analiza las siguientes notas de intervenciones clínicas y proporciona:
                    1. Un resumen conciso del progreso del couder
                    2. Puntos clave observados
                    3. Un diagnóstico preliminar basado en las observaciones
                    4. Sugerencias específicas para continuar el proceso
                    5. Nivel de riesgo (bajo, medio, alto)
                    6. Recomendaciones para el equipo
                    
                    Responde en formato JSON con las siguientes claves:
                    - resumen
                    - puntos_clave (array de strings)
                    - diagnostico_preliminar
                    - sugerencias (array de strings)
                    - nivel_riesgo
                    - recomendaciones (array de strings)"""
                },
                {
                    "role": "user",
                    "content": context
                }
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        try:
            content = response.choices[0].message.content
            import json
            analysis = json.loads(content)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            analysis = {
                "resumen": response.choices[0].message.content,
                "puntos_clave": [],
                "diagnostico_preliminar": "No disponible",
                "sugerencias": [],
                "nivel_riesgo": "medio",
                "recomendaciones": []
            }
        
        # Save analysis to MongoDB
        analysis_record = {
            "couder_id": couder_id,
            "tipo_analisis": "sintesis",
            "contenido": analysis,
            "intervenciones_incluidas": intervention_ids,
            "fecha_generacion": datetime.utcnow(),
            "modelo_ia": "gpt-4",
            "version": "1.0"
        }
        
        mongo_db.ai_analisis.insert_one(analysis_record)
        
        return analysis
    
    async def generate_diagnosis(self, couder_id: int, intervention_ids: List[int]) -> Dict[str, Any]:
        """Generate mini-diagnosis based on interventions"""
        if not self.client:
            raise Exception("OpenAI API key not configured")
        
        mongo_db = get_mongo_db()
        
        # Get clinical records
        records = list(mongo_db.historial_clinico.find({
            "couder_id": couder_id,
            "intervencion_id": {"$in": intervention_ids}
        }).sort("fecha_registro", 1))
        
        if not records:
            raise Exception("No clinical records found for diagnosis")
        
        # Prepare context
        context = self._prepare_diagnosis_context(records)
        
        # Generate diagnosis
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """Eres un psicólogo clínico experto. Basado en las notas de intervenciones, 
                    proporciona un diagnóstico preliminar conciso y sugerencias específicas.
                    
                    Responde en formato JSON con:
                    - diagnostico_preliminar: diagnóstico breve y claro
                    - sugerencias: array de 3-5 sugerencias prácticas
                    - areas_atencion: áreas clave a monitorear
                    - pronostico: pronóstico breve (positivo, reservado, requiere atención)"""
                },
                {
                    "role": "user",
                    "content": context
                }
            ],
            temperature=0.2,
            max_tokens=800
        )
        
        try:
            content = response.choices[0].message.content
            import json
            diagnosis = json.loads(content)
        except json.JSONDecodeError:
            diagnosis = {
                "diagnostico_preliminar": response.choices[0].message.content,
                "sugerencias": [],
                "areas_atencion": [],
                "pronostico": "requiere evaluación adicional"
            }
        
        # Save diagnosis
        diagnosis_record = {
            "couder_id": couder_id,
            "tipo_analisis": "diagnostico",
            "contenido": diagnosis,
            "intervenciones_incluidas": intervention_ids,
            "fecha_generacion": datetime.utcnow(),
            "modelo_ia": "gpt-4",
            "version": "1.0"
        }
        
        mongo_db.ai_analisis.insert_one(diagnosis_record)
        
        return diagnosis
    
    async def get_historical_analyses(self, couder_id: int, analysis_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get historical AI analyses for a couder"""
        mongo_db = get_mongo_db()
        
        query = {"couder_id": couder_id}
        if analysis_type:
            query["tipo_analisis"] = analysis_type
        
        analyses = list(mongo_db.ai_analisis.find(query).sort("fecha_generacion", -1))
        
        # Convert ObjectId to string
        for analysis in analyses:
            if "_id" in analysis:
                analysis["_id"] = str(analysis["_id"])
            if "fecha_generacion" in analysis:
                analysis["fecha_generacion"] = analysis["fecha_generacion"].isoformat()
        
        return analyses
    
    def _prepare_synthesis_context(self, records: List[Dict[str, Any]]) -> str:
        """Prepare context for AI synthesis"""
        context = "Notas de intervenciones clínicas:\n\n"
        
        for i, record in enumerate(records, 1):
            fecha = record.get("fecha_registro", "").strftime("%Y-%m-%d") if record.get("fecha_registro") else "Fecha no disponible"
            context += f"Intervención {i} ({fecha}):\n"
            context += f"Notas: {record.get('notas_completas', 'No disponibles')}\n"
            context += f"Estado emocional: {record.get('estado_emocional', 'No registrado')}\n"
            context += f"Nivel de participación: {record.get('nivel_participacion', 'No evaluado')}\n"
            context += f"Observaciones: {record.get('observaciones_adicionales', 'Sin observaciones')}\n\n"
        
        return context
    
    def _prepare_diagnosis_context(self, records: List[Dict[str, Any]]) -> str:
        """Prepare context for AI diagnosis"""
        context = "Historial de intervenciones para diagnóstico:\n\n"
        
        for i, record in enumerate(records, 1):
            fecha = record.get("fecha_registro", "").strftime("%Y-%m-%d") if record.get("fecha_registro") else "Fecha no disponible"
            context += f"Intervención {i} ({fecha}):\n"
            context += f"Síntomas observados: {', '.join(record.get('sintomas_observados', []))}\n"
            context += f"Estado emocional: {record.get('estado_emocional', 'No registrado')}\n"
            context += f"Nivel de participación: {record.get('nivel_participacion', 'No evaluado')}\n"
            context += f"Notas principales: {record.get('notas_completas', 'No disponibles')[:200]}...\n\n"
        
        return context

# Global AI service instance
ai_service = AIService()
