#!/usr/bin/env python3
"""
Script de migración para el sistema RIWI
Crea tablas basadas en los scripts reales y carga datos CSV
"""

import sys
import os
import csv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import (
    Campus, Cohort, Clan, Coder, Specialist, 
    LearningPath, History, AIReport
)

def create_tables():
    """Create all database tables"""
    print("🔨 Creating database tables...")
    
    # Use postgres user to create tables with proper privileges
    admin_engine = create_engine("postgresql://postgres:2846@localhost:5432/riwi_interventions")
    Base.metadata.create_all(bind=admin_engine)
    admin_engine.dispose()
    
    print("✅ Database tables created successfully!")

def load_csv_data(filepath, table_name):
    """Load data from CSV file"""
    if not os.path.exists(filepath):
        print(f"⚠️  File {filepath} not found, skipping...")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    
    print(f"📖 Loaded {len(data)} records from {table_name}")
    return data

def migrate_campuses(session):
    """Migrate campus data"""
    print("\n🏢 Migrating Campuses...")
    data = load_csv_data('data/campus.csv', 'campus')
    
    for row in data:
        campus = Campus(
            id_campus=int(row['id_campus']),
            campus_name=row['campus_name']
        )
        session.add(campus)
    
    session.commit()
    print(f"✅ Migrated {len(data)} campuses")

def migrate_cohorts(session):
    """Migrate cohort data"""
    print("\n📚 Migrating Cohorts...")
    data = load_csv_data('data/cohort.csv', 'cohort')
    
    for row in data:
        cohort = Cohort(
            id_cohort=int(row['id_cohort']),
            name_cohort=row['name_cohort'],
            start_date=datetime.strptime(row['start_date'], '%Y-%m-%d').date(),
            status=row['status'],
            id_campus=int(row['id_campus'])
        )
        session.add(cohort)
    
    session.commit()
    print(f"✅ Migrated {len(data)} cohorts")

def migrate_clans(session):
    """Migrate clan data"""
    print("\n👥 Migrating Clans...")
    data = load_csv_data('data/clan.csv', 'clan')
    
    for row in data:
        clan = Clan(
            id_clan=int(row['id_clan']),
            name_clan=row['name_clan'],
            shift=row['shift'],
            id_cohort=int(row['id_cohort'])
        )
        session.add(clan)
    
    session.commit()
    print(f"✅ Migrated {len(data)} clans")

def migrate_specialists(session):
    """Migrate specialist data"""
    print("\n👨‍⚕️ Migrating Specialists...")
    data = load_csv_data('data/specialist.csv', 'specialist')
    
    for row in data:
        specialist = Specialist(
            id_specialist=int(row['id_specialist']),
            name_specialist=row['name_specialist'],
            email=row['email'],
            password=row['password']  # In production, this should be properly hashed
        )
        session.add(specialist)
    
    session.commit()
    print(f"✅ Migrated {len(data)} specialists")

def migrate_coders(session):
    """Migrate coder data"""
    print("\n💻 Migrating Coders...")
    data = load_csv_data('data/coder.csv', 'coder')
    
    for row in data:
        coder = Coder(
            id_coder=int(row['id_coder']),
            full_name=row['full_name'],
            document_id=row['document_id'],
            birth_date=datetime.strptime(row['birth_date'], '%Y-%m-%d').date(),
            status=row['status'],
            withdrawal_date=datetime.strptime(row['withdrawal_date'], '%Y-%m-%d').date(),
            average=float(row['average']) if row['average'] else None,
            id_clan=int(row['id_clan'])
        )
        session.add(coder)
    
    session.commit()
    print(f"✅ Migrated {len(data)} coders")

def migrate_learning_paths(session):
    """Migrate learning path data"""
    print("\n🛤️ Migrating Learning Paths...")
    data = load_csv_data('data/learning_path.csv', 'learning_path')
    
    for row in data:
        learning_path = LearningPath(
            id_path=int(row['id_path']),
            route_type=row['route_type'],
            current_path=int(row['current_path']),
            clan_average=float(row['clan_average']) if row['clan_average'] else None,
            id_coder=int(row['id_coder'])
        )
        session.add(learning_path)
    
    session.commit()
    print(f"✅ Migrated {len(data)} learning paths")

def migrate_histories(session):
    """Migrate history data"""
    print("\n📝 Migrating Histories...")
    data = load_csv_data('data/history.csv', 'history')
    
    for row in data:
        history = History(
            id_history=int(row['id_history']),
            intervention_type=row['intervention_type'],
            description=row['description'],
            ai_micro=row['ai_micro'],
            date_time=datetime.strptime(row['date_time'], '%Y-%m-%d %H:%M:%S'),
            id_specialist=int(row['id_specialist']),
            id_coder=int(row['id_coder'])
        )
        session.add(history)
    
    session.commit()
    print(f"✅ Migrated {len(data)} histories")

def migrate_ai_reports(session):
    """Migrate AI report data"""
    print("\n🤖 Migrating AI Reports...")
    data = load_csv_data('data/ai_report.csv', 'ai_report')
    
    for row in data:
        ai_report = AIReport(
            id_reporte=int(row['id_reporte']),
            period_type=row['period_type'],
            diagnosis=row['diagnosis'],
            risk_level=row['risk_level'],
            generated_at=datetime.strptime(row['generated_at'], '%Y-%m-%d %H:%M:%S'),
            id_coder=int(row['id_coder'])
        )
        session.add(ai_report)
    
    session.commit()
    print(f"✅ Migrated {len(data)} AI reports")

def verify_migration(session):
    """Verify migration results"""
    print("\n🔍 Verifying migration...")
    
    counts = {
        'Campus': session.query(Campus).count(),
        'Cohort': session.query(Cohort).count(),
        'Clan': session.query(Clan).count(),
        'Specialist': session.query(Specialist).count(),
        'Coder': session.query(Coder).count(),
        'Learning Path': session.query(LearningPath).count(),
        'History': session.query(History).count(),
        'AI Report': session.query(AIReport).count()
    }
    
    print("\n📊 Migration Summary:")
    total = 0
    for table, count in counts.items():
        print(f"   {table}: {count:,} records")
        total += count
    
    print(f"\n🎯 Total Records Migrated: {total:,}")
    
    return counts

def main():
    """Main migration function"""
    print("🚀 Starting RIWI Database Migration...")
    print(f"📁 Database URL: {settings.database_url}")
    
    try:
        # Create database tables
        create_tables()
        
        # Create session
        engine = create_engine(settings.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        # Migrate all data
        migrate_campuses(session)
        migrate_cohorts(session)
        migrate_clans(session)
        migrate_specialists(session)
        migrate_coders(session)
        migrate_learning_paths(session)
        migrate_histories(session)
        migrate_ai_reports(session)
        
        # Verify migration
        verify_migration(session)
        
        session.close()
        
        print("\n🎉 Migration completed successfully!")
        print("🌐 Database is ready for RIWI System!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
