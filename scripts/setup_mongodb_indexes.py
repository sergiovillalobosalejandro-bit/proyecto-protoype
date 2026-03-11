#!/usr/bin/env python3
"""
Setup MongoDB indexes for optimal performance
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from pymongo import MongoClient
from app.core.config import settings

def setup_indexes():
    """Create optimized indexes for MongoDB collections"""
    
    try:
        client = MongoClient(settings.mongodb_url)
        db = client.clinical_records
        
        print("🔧 Setting up MongoDB indexes...")
        
        # Historial Clínico indexes
        print("📝 Setting up historial_clinico indexes...")
        historial_indexes = [
            # Primary lookup index
            [("couder_id", 1), ("fecha_registro", -1)],
            # Intervention lookup
            [("intervencion_id", 1)],
            # Date range queries
            [("fecha_registro", -1)],
            # Compound index for common queries
            [("couder_id", 1), ("intervencion_id", 1), ("fecha_registro", -1)]
        ]
        
        for index in historial_indexes:
            result = db.historial_clinico.create_index(index)
            print(f"  ✅ Created index: {index} -> {result}")
        
        # AI Análisis indexes
        print("🤖 Setting up ai_analisis indexes...")
        ai_indexes = [
            # Primary lookup index
            [("couder_id", 1), ("fecha_generacion", -1)],
            # Type-based queries
            [("tipo_analisis", 1)],
            # Date range queries
            [("fecha_generacion", -1)],
            # Compound index for analytics
            [("tipo_analisis", 1), ("fecha_generacion", -1)]
        ]
        
        for index in ai_indexes:
            result = db.ai_analisis.create_index(index)
            print(f"  ✅ Created index: {index} -> {result}")
        
        # Audio Registros indexes
        print("🎵 Setting up audio_registros indexes...")
        audio_indexes = [
            # Primary lookup index
            [("couder_id", 1), ("fecha_grabacion", -1)],
            # User-based queries
            [("usuario_id", 1)],
            # Date range queries
            [("fecha_grabacion", -1)],
            # File path lookup
            [("archivo_path", 1)],
            # Compound index for user-couder queries
            [("usuario_id", 1), ("couder_id", 1), ("fecha_grabacion", -1)]
        ]
        
        for index in audio_indexes:
            result = db.audio_registros.create_index(index)
            print(f"  ✅ Created index: {index} -> {result}")
        
        # Seguimiento Progreso indexes
        print("📊 Setting up seguimiento_progreso indexes...")
        seguimiento_indexes = [
            # Primary lookup index
            [("couder_id", 1), ("fecha_evaluacion", -1)],
            # Date range queries
            [("fecha_evaluacion", -1)],
            # Metric-based queries (if metric fields are indexed)
            [("metricas.nivel_riesgo", 1)],
            # Compound index for progress tracking
            [("couder_id", 1), ("fecha_evaluacion", -1), ("metricas.estado", 1)]
        ]
        
        for index in seguimiento_indexes:
            result = db.seguimiento_progreso.create_index(index)
            print(f"  ✅ Created index: {index} -> {result}")
        
        # Create TTL index for old logs (optional)
        print("⏰ Setting up TTL index for old data...")
        
        # Auto-delete audio records older than 2 years (optional)
        try:
            result = db.audio_registros.create_index(
                [("fecha_grabacion", 1)],
                expireAfterSeconds=2 * 365 * 24 * 60 * 60  # 2 years
            )
            print(f"  ✅ Created TTL index for audio_registros: {result}")
        except Exception as e:
            print(f"  ⚠️  Could not create TTL index: {e}")
        
        # Get index statistics
        print("\n📊 Index Statistics:")
        collections = ["historial_clinico", "ai_analisis", "audio_registros", "seguimiento_progreso"]
        
        for collection_name in collections:
            collection = db[collection_name]
            indexes = collection.list_indexes()
            print(f"\n  {collection_name}:")
            for index in indexes:
                index_name = index["name"]
                index_keys = index["key"]
                print(f"    📋 {index_name}: {index_keys}")
        
        client.close()
        print("\n🎉 MongoDB indexes setup completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up indexes: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Starting MongoDB index setup for Clinical Intervention Tracking System")
    print("=" * 60)
    
    # Check environment variables
    if not settings.mongodb_url:
        print("❌ MONGODB_URL environment variable not set")
        return False
    
    success = setup_indexes()
    
    if success:
        print("\n✅ Index setup completed!")
        print("📈 Performance improvements:")
        print("  - Faster couder history lookups")
        print("  - Optimized AI analysis queries")
        print("  - Improved audio file searches")
        print("  - Better progress tracking performance")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
