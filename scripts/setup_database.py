#!/usr/bin/env python3
"""
Database setup script for the Clinical Intervention Tracking System
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from sqlalchemy import create_engine, text
from pymongo import MongoClient
from app.core.config import settings
from app.core.database import Base

def setup_postgresql():
    """Setup PostgreSQL database"""
    print("Setting up PostgreSQL database...")
    
    # Create engine
    engine = create_engine(settings.database_url)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ PostgreSQL tables created successfully")
    
    # Create sample data
    create_sample_data(engine)

def create_sample_data(engine):
    """Create sample data for testing"""
    from app.models import Sede, Corte, Clan, Usuario, Couder, EstadoCouder, TipoRuta, Jornada, RolUsuario
    from sqlalchemy.orm import sessionmaker
    from passlib.context import CryptContext
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Sede).first():
            print("Sample data already exists, skipping...")
            return
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Create sample user
        admin_user = Usuario(
            username="admin",
            email="admin@clinical.com",
            nombre_completo="Administrador del Sistema",
            hashed_password=pwd_context.hash("admin123"),
            rol=RolUsuario.ADMIN
        )
        db.add(admin_user)
        
        # Create sample sede
        sede = Sede(
            nombre="Sede Principal",
            direccion="Calle 123 #45-67",
            telefono="3001234567",
            email="principal@clinical.com"
        )
        db.add(sede)
        db.flush()
        
        # Create sample corte
        corte = Corte(
            nombre="Corte 2024-1",
            sede_id=sede.id,
            fecha_inicio="2024-01-15T08:00:00",
            fecha_fin="2024-06-15T17:00:00",
            tipo_ruta=TipoRuta.BASICA
        )
        db.add(corte)
        db.flush()
        
        # Create sample clans
        clan_am = Clan(
            nombre="Clan A1",
            corte_id=corte.id,
            jornada=Jornada.AM,
            capacidad_maxima=25
        )
        db.add(clan_am)
        
        clan_pm = Clan(
            nombre="Clan B1",
            corte_id=corte.id,
            jornada=Jornada.PM,
            capacidad_maxima=25
        )
        db.add(clan_pm)
        db.flush()
        
        # Create sample couders
        couder1 = Couder(
            cc="123456789",
            nombre_completo="Juan Pérez González",
            fecha_nacimiento="2005-03-15",
            telefono="3009876543",
            email="juan.perez@email.com",
            direccion="Carrera 7 #12-34",
            clan_id=clan_am.id,
            estado=EstadoCouder.ACTIVO
        )
        db.add(couder1)
        
        couder2 = Couder(
            cc="987654321",
            nombre_completo="María Rodríguez López",
            fecha_nacimiento="2006-07-22",
            telefono="3012345678",
            email="maria.rodriguez@email.com",
            direccion="Avenida 5 #67-89",
            clan_id=clan_pm.id,
            estado=EstadoCouder.ACTIVO
        )
        db.add(couder2)
        
        db.commit()
        print("✅ Sample data created successfully")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

def setup_mongodb():
    """Setup MongoDB collections"""
    print("Setting up MongoDB collections...")
    
    try:
        client = MongoClient(settings.mongodb_url)
        db = client.clinical_records
        
        # Create collections with validation
        collections_config = [
            {
                "name": "historial_clinico",
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["couder_id", "intervencion_id", "fecha_registro"],
                        "properties": {
                            "couder_id": {"bsonType": "int"},
                            "intervencion_id": {"bsonType": "int"},
                            "notas_completas": {"bsonType": "string"},
                            "fecha_registro": {"bsonType": "date"}
                        }
                    }
                }
            },
            {
                "name": "ai_analisis",
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["couder_id", "tipo_analisis", "fecha_generacion", "contenido"],
                        "properties": {
                            "couder_id": {"bsonType": "int"},
                            "tipo_analisis": {"bsonType": "string"},
                            "contenido": {"bsonType": "object"},
                            "fecha_generacion": {"bsonType": "date"}
                        }
                    }
                }
            },
            {
                "name": "audio_registros",
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["couder_id", "usuario_id", "fecha_grabacion", "archivo_path"],
                        "properties": {
                            "couder_id": {"bsonType": "int"},
                            "usuario_id": {"bsonType": "int"},
                            "fecha_grabacion": {"bsonType": "date"},
                            "archivo_path": {"bsonType": "string"}
                        }
                    }
                }
            },
            {
                "name": "seguimiento_progreso",
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["couder_id", "fecha_evaluacion", "metricas"],
                        "properties": {
                            "couder_id": {"bsonType": "int"},
                            "fecha_evaluacion": {"bsonType": "date"},
                            "metricas": {"bsonType": "object"}
                        }
                    }
                }
            }
        ]
        
        for collection_config in collections_config:
            try:
                # Drop collection if it exists
                if collection_config["name"] in db.list_collection_names():
                    db.drop_collection(collection_config["name"])
                
                # Create collection with validation
                db.create_collection(
                    collection_config["name"],
                    validator=collection_config["validator"]
                )
                
                # Create indexes
                if collection_config["name"] == "historial_clinico":
                    db[collection_config["name"]].create_index([("couder_id", 1), ("fecha_registro", -1)])
                    db[collection_config["name"]].create_index([("intervencion_id", 1)])
                elif collection_config["name"] == "ai_analisis":
                    db[collection_config["name"]].create_index([("couder_id", 1), ("fecha_generacion", -1)])
                    db[collection_config["name"]].create_index([("tipo_analisis", 1)])
                elif collection_config["name"] == "audio_registros":
                    db[collection_config["name"]].create_index([("couder_id", 1), ("fecha_grabacion", -1)])
                    db[collection_config["name"]].create_index([("usuario_id", 1)])
                elif collection_config["name"] == "seguimiento_progreso":
                    db[collection_config["name"]].create_index([("couder_id", 1), ("fecha_evaluacion", -1)])
                
                print(f"✅ Collection '{collection_config['name']}' created successfully")
                
            except Exception as e:
                print(f"❌ Error creating collection '{collection_config['name']}': {e}")
        
        client.close()
        print("✅ MongoDB setup completed")
        
    except Exception as e:
        print(f"❌ MongoDB setup failed: {e}")

def main():
    """Main setup function"""
    print("🚀 Starting database setup for Clinical Intervention Tracking System")
    print("=" * 60)
    
    # Check environment variables
    if not settings.database_url:
        print("❌ DATABASE_URL environment variable not set")
        return False
    
    if not settings.mongodb_url:
        print("❌ MONGODB_URL environment variable not set")
        return False
    
    try:
        # Setup PostgreSQL
        setup_postgresql()
        
        print()
        
        # Setup MongoDB
        setup_mongodb()
        
        print()
        print("🎉 Database setup completed successfully!")
        print()
        print("Next steps:")
        print("1. Start the backend server: python run.py")
        print("2. Open frontend/index.html in your browser")
        print("3. Login with: admin / admin123")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
