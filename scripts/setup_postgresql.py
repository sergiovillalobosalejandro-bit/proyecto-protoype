#!/usr/bin/env python3
"""
Script de configuración para PostgreSQL - Sistema RIWI
Crea base de datos, usuario y configuración inicial
"""

import psycopg2
from psycopg2 import sql
import sys
import os

# Configuration
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "2846"
NEW_DB_NAME = "riwi_interventions"
NEW_USER = "riwi_user"
NEW_USER_PASSWORD = "riwi_password"

def create_connection(database="postgres"):
    """Create connection to PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=database
        )
        conn.autocommit = True
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        print("\n💡 Solución:")
        print("1. Asegúrate que PostgreSQL esté corriendo")
        print("2. Verifica el usuario y contraseña en el .env")
        print("3. Ejecuta este script con permisos de administrador")
        return None

def create_database(conn):
    """Create the main database"""
    try:
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (NEW_DB_NAME,)
        )
        
        if cursor.fetchone():
            print(f"✅ Database '{NEW_DB_NAME}' already exists")
        else:
            # Create database
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(NEW_DB_NAME))
            )
            print(f"✅ Database '{NEW_DB_NAME}' created successfully")
        
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_user(conn):
    """Create dedicated user for the application"""
    try:
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute(
            "SELECT 1 FROM pg_roles WHERE rolname = %s",
            (NEW_USER,)
        )
        
        if cursor.fetchone():
            print(f"✅ User '{NEW_USER}' already exists")
        else:
            # Create user
            cursor.execute(
                sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
                    sql.Identifier(NEW_USER)
                ),
                (NEW_USER_PASSWORD,)
            )
            print(f"✅ User '{NEW_USER}' created successfully")
        
        # Grant privileges
        cursor.execute(
            sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                sql.Identifier(NEW_DB_NAME),
                sql.Identifier(NEW_USER)
            )
        )
        print(f"✅ Privileges granted to '{NEW_USER}'")
        
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error creating user: {e}")
        return False

def test_connection():
    """Test connection to the new database"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=NEW_USER,
            password=NEW_USER_PASSWORD,
            database=NEW_DB_NAME
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        
        print(f"✅ Connection test successful!")
        print(f"📊 PostgreSQL: {version.split(',')[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Connection test failed: {e}")
        return False

def update_env_file():
    """Update .env file with new database credentials"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    
    try:
        # Read current .env
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Update database URL
        new_db_url = f"postgresql://{NEW_USER}:{NEW_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{NEW_DB_NAME}"
        
        updated_lines = []
        for line in lines:
            if line.startswith('DATABASE_URL='):
                updated_lines.append(f'DATABASE_URL={new_db_url}\n')
            else:
                updated_lines.append(line)
        
        # Write updated .env
        with open(env_path, 'w') as f:
            f.writelines(updated_lines)
        
        print(f"✅ .env file updated with new database URL")
        return True
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up PostgreSQL for RIWI System...")
    print(f"📁 Host: {DB_HOST}:{DB_PORT}")
    print(f"👤 Admin User: {DB_USER}")
    print(f"🗄️  New Database: {NEW_DB_NAME}")
    print(f"👤 New User: {NEW_USER}")
    print()
    
    # Step 1: Connect to PostgreSQL
    print("📡 Connecting to PostgreSQL...")
    conn = create_connection()
    if not conn:
        sys.exit(1)
    
    # Step 2: Create database
    print("\n🗄️  Creating database...")
    if not create_database(conn):
        conn.close()
        sys.exit(1)
    
    # Step 3: Create user
    print("\n👤 Creating user...")
    if not create_user(conn):
        conn.close()
        sys.exit(1)
    
    conn.close()
    
    # Step 4: Test connection
    print("\n🧪 Testing connection...")
    if not test_connection():
        sys.exit(1)
    
    # Step 5: Update .env file
    print("\n📝 Updating configuration...")
    if not update_env_file():
        sys.exit(1)
    
    print("\n🎉 PostgreSQL setup completed successfully!")
    print("\n📋 Summary:")
    print(f"   Database: {NEW_DB_NAME}")
    print(f"   User: {NEW_USER}")
    print(f"   URL: postgresql://{NEW_USER}:****@{DB_HOST}:{DB_PORT}/{NEW_DB_NAME}")
    print("\n🚀 Ready for database migration!")
    print("   Run: python scripts/migrate_database.py")

if __name__ == "__main__":
    main()
