#!/usr/bin/env python3
"""
Create admin user script for the Clinical Intervention Tracking System
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.core.config import settings
from app.models import Usuario, RolUsuario
from passlib.context import CryptContext

def create_admin_user(username="admin", password="admin123", email="admin@clinical.com", full_name="Administrador"):
    """Create admin user"""
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(Usuario).filter(Usuario.username == username).first()
        if existing_user:
            print(f"❌ User '{username}' already exists")
            return False
        
        # Create admin user
        admin_user = Usuario(
            username=username,
            email=email,
            nombre_completo=full_name,
            hashed_password=pwd_context.hash(password),
            rol=RolUsuario.ADMIN
        )
        
        db.add(admin_user)
        db.commit()
        
        print(f"✅ Admin user '{username}' created successfully")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create admin user")
    parser.add_argument("--username", default="admin", help="Username (default: admin)")
    parser.add_argument("--password", default="admin123", help="Password (default: admin123)")
    parser.add_argument("--email", default="admin@clinical.com", help="Email")
    parser.add_argument("--name", default="Administrador", help="Full name")
    
    args = parser.parse_args()
    
    print("🔧 Creating admin user...")
    
    success = create_admin_user(
        username=args.username,
        password=args.password,
        email=args.email,
        full_name=args.name
    )
    
    if success:
        print("\n🎉 Admin user created successfully!")
        print("You can now login to the system with these credentials.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
