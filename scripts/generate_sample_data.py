#!/usr/bin/env python3
"""
Script para generar datos de muestra para el sistema RIWI
Crea 200+ registros de coders con datos realistas
"""

import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import os

# Initialize Faker
fake = Faker(['es_ES', 'en_US'])

# Configuration
NUM_CAMPUS = 5
NUM_COHORTS_PER_CAMPUS = 3
NUM_CLANS_PER_COHORT = 4
NUM_CODERS_PER_CLAN = 15
NUM_SPECIALISTS = 20
NUM_HISTORIES_PER_CODER = 5
NUM_AI_REPORTS_PER_CODER = 3

# Generate data
def generate_campuses():
    """Generate campus data"""
    campuses = []
    campus_names = [
        "Campus Principal", "Campus Norte", "Campus Sur", 
        "Campus Este", "Campus Oeste"
    ]
    
    for i, name in enumerate(campus_names[:NUM_CAMPUS], 1):
        campuses.append({
            'id_campus': i,
            'campus_name': name
        })
    
    return campuses

def generate_cohorts(campuses):
    """Generate cohort data"""
    cohorts = []
    cohort_id = 1
    
    for campus in campuses:
        for i in range(NUM_COHORTS_PER_CAMPUS):
            start_date = fake.date_between(start_date='-2y', end_date='-6m')
            status = random.choice(['ACTIVE', 'INACTIVE', 'COMPLETED', 'SUSPENDED'])
            
            cohorts.append({
                'id_cohort': cohort_id,
                'name_cohort': f"Cohort {cohort_id} - {campus['campus_name']}",
                'start_date': start_date.strftime('%Y-%m-%d'),
                'status': status,
                'id_campus': campus['id_campus']
            })
            cohort_id += 1
    
    return cohorts

def generate_clans(cohorts):
    """Generate clan data"""
    clans = []
    clan_id = 1
    
    for cohort in cohorts:
        for i in range(NUM_CLANS_PER_COHORT):
            shift = random.choice(['MORNING', 'AFTERNOON', 'NIGHT', 'FULL_TIME'])
            
            clans.append({
                'id_clan': clan_id,
                'name_clan': f"Clan {chr(65 + i)} - Cohort {cohort['id_cohort']}",
                'shift': shift,
                'id_cohort': cohort['id_cohort']
            })
            clan_id += 1
    
    return clans

def generate_specialists():
    """Generate specialist data"""
    specialists = []
    specialties = ['Psicología', 'Terapia Ocupacional', 'Trabajo Social', 'Pedagogía', 'Psiquiatría']
    
    for i in range(1, NUM_SPECIALISTS + 1):
        specialists.append({
            'id_specialist': i,
            'name_specialist': fake.name(),
            'email': fake.email(),
            'password': 'hashed_password_123'  # In real app, this would be properly hashed
        })
    
    return specialists

def generate_coders(clans):
    """Generate coder data"""
    coders = []
    coder_id = 1
    
    for clan in clans:
        for i in range(NUM_CODERS_PER_CLAN):
            birth_date = fake.date_between(start_date='-25y', end_date='-16y')
            status = random.choice(['ACTIVE', 'ACTIVE', 'ACTIVE', 'WITHDRAWN', 'COMPLETED'])  # More active
            withdrawal_date = birth_date if status == 'WITHDRAWN' else fake.date_between(start_date='-1y', end_date='today')
            average = round(random.uniform(6.0, 9.5), 2) if status == 'COMPLETED' else None
            
            coders.append({
                'id_coder': coder_id,
                'full_name': fake.name(),
                'document_id': f"{random.randint(80000000, 99999999)}",
                'birth_date': birth_date.strftime('%Y-%m-%d'),
                'status': status,
                'withdrawal_date': withdrawal_date.strftime('%Y-%m-%d'),
                'average': average,
                'id_clan': clan['id_clan']
            })
            coder_id += 1
    
    return coders

def generate_learning_paths(coders):
    """Generate learning path data"""
    learning_paths = []
    
    for coder in coders:
        route_type = random.choice(['básica', 'avanzada', 'intensiva'])
        current_path = random.randint(1, 12)
        clan_average = round(random.uniform(6.0, 9.5), 2) if coder['status'] == 'completed' else None
        
        learning_paths.append({
            'id_path': coder['id_coder'],
            'route_type': route_type,
            'current_path': current_path,
            'clan_average': clan_average,
            'id_coder': coder['id_coder']
        })
    
    return learning_paths

def generate_histories(coders, specialists):
    """Generate history data"""
    histories = []
    history_id = 1
    
    intervention_types = [
        'Evaluación inicial', 'Seguimiento individual', 'Intervención grupal',
        'Apoyo académico', 'Intervención familiar', 'Crisis emocional',
        'Plan de acción', 'Evaluación de progreso', 'Derivación',
        'Cierre de caso'
    ]
    
    for coder in coders:
        num_histories = random.randint(1, NUM_HISTORIES_PER_CODER)
        
        for i in range(num_histories):
            specialist = random.choice(specialists)
            date_time = fake.date_time_between(start_date='-6m', end_date='now')
            intervention_type = random.choice(intervention_types)
            description = fake.paragraph(nb_sentences=3)
            ai_micro = fake.paragraph(nb_sentences=2)
            
            histories.append({
                'id_history': history_id,
                'intervention_type': intervention_type,
                'description': description,
                'ai_micro': ai_micro,
                'date_time': date_time.strftime('%Y-%m-%d %H:%M:%S'),
                'id_specialist': specialist['id_specialist'],
                'id_coder': coder['id_coder']
            })
            history_id += 1
    
    return histories

def generate_ai_reports(coders):
    """Generate AI report data"""
    ai_reports = []
    report_id = 1
    
    risk_levels = ['low', 'medium', 'high']
    period_types = ['mensual', 'trimestral', 'semestral']
    
    for coder in coders:
        if coder['status'] in ['active', 'completed']:
            num_reports = random.randint(1, NUM_AI_REPORTS_PER_CODER)
            
            for i in range(num_reports):
                period_type = random.choice(period_types)
                risk_level = random.choice(risk_levels)
                diagnosis = fake.paragraph(nb_sentences=5)
                generated_at = fake.date_time_between(start_date='-3m', end_date='now')
                
                ai_reports.append({
                    'id_reporte': report_id,
                    'period_type': period_type,
                    'diagnosis': diagnosis,
                    'risk_level': risk_level,
                    'generated_at': generated_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'id_coder': coder['id_coder']
                })
                report_id += 1
    
    return ai_reports

def write_csv(data, filename, fieldnames):
    """Write data to CSV file"""
    os.makedirs('data', exist_ok=True)
    filepath = os.path.join('data', filename)
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✅ Generated {filename} with {len(data)} records")

def main():
    """Main function to generate all sample data"""
    print("🚀 Generating sample data for RIWI System...")
    
    # Generate all data
    campuses = generate_campuses()
    cohorts = generate_cohorts(campuses)
    clans = generate_clans(cohorts)
    specialists = generate_specialists()
    coders = generate_coders(clans)
    learning_paths = generate_learning_paths(coders)
    histories = generate_histories(coders, specialists)
    ai_reports = generate_ai_reports(coders)
    
    # Write CSV files
    write_csv(campuses, 'campus.csv', ['id_campus', 'campus_name'])
    write_csv(cohorts, 'cohort.csv', ['id_cohort', 'name_cohort', 'start_date', 'status', 'id_campus'])
    write_csv(clans, 'clan.csv', ['id_clan', 'name_clan', 'shift', 'id_cohort'])
    write_csv(specialists, 'specialist.csv', ['id_specialist', 'name_specialist', 'email', 'password'])
    write_csv(coders, 'coder.csv', ['id_coder', 'full_name', 'document_id', 'birth_date', 'status', 'withdrawal_date', 'average', 'id_clan'])
    write_csv(learning_paths, 'learning_path.csv', ['id_path', 'route_type', 'current_path', 'clan_average', 'id_coder'])
    write_csv(histories, 'history.csv', ['id_history', 'intervention_type', 'description', 'ai_micro', 'date_time', 'id_specialist', 'id_coder'])
    write_csv(ai_reports, 'ai_report.csv', ['id_reporte', 'period_type', 'diagnosis', 'risk_level', 'generated_at', 'id_coder'])
    
    # Summary
    total_records = len(campuses) + len(cohorts) + len(clans) + len(specialists) + len(coders) + len(learning_paths) + len(histories) + len(ai_reports)
    
    print("\n📊 Summary:")
    print(f"   Campuses: {len(campuses)}")
    print(f"   Cohorts: {len(cohorts)}")
    print(f"   Clans: {len(clans)}")
    print(f"   Specialists: {len(specialists)}")
    print(f"   Coders: {len(coders)}")
    print(f"   Learning Paths: {len(learning_paths)}")
    print(f"   Histories: {len(histories)}")
    print(f"   AI Reports: {len(ai_reports)}")
    print(f"   Total Records: {total_records}")
    
    print(f"\n📁 CSV files saved in 'data/' directory")
    print("🎯 Ready for database migration!")

if __name__ == "__main__":
    main()
