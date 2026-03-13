from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
# Temporarily disable legacy APIs to avoid conflicts
# from .api import auth, couders, intervenciones, dashboard, ai, audio
from .api import campus, cohorts, clans, coders, specialists, histories, auth_simple
from .core.database import engine
from .models import Base
from .middleware import LoggingMiddleware, SecurityMiddleware

# Create database tables (only if database is available)
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
except Exception as e:
    print(f"⚠️  Database not available yet: {e}")
    print("   Run 'python scripts/setup_database.py' after setting up databases")

app = FastAPI(
    title="RIWI - Sistema de Intervenciones de Couders",
    description="Sistema de registro individual de intervenciones de couders para RIWI",
    version="1.0.0"
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(SecurityMiddleware, calls_per_minute=100)
app.add_middleware(LoggingMiddleware)

# Include API routers
# Include API routers (only new models for now)
# app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
# app.include_router(couders.router, prefix="/api/couders", tags=["couders"])
# app.include_router(intervenciones.router, prefix="/api/intervenciones", tags=["intervenciones"])
# app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
# app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
# app.include_router(audio.router, prefix="/api/audio", tags=["audio"])

# New API routers based on real database structure
app.include_router(auth_simple.router, prefix="/api/auth", tags=["authentication"])
app.include_router(campus.router, prefix="/api/campus", tags=["campus"])
app.include_router(cohorts.router, prefix="/api/cohorts", tags=["cohorts"])
app.include_router(clans.router, prefix="/api/clans", tags=["clans"])
app.include_router(coders.router, prefix="/api/coders", tags=["coders"])
app.include_router(specialists.router, prefix="/api/specialists", tags=["specialists"])
app.include_router(histories.router, prefix="/api/histories", tags=["histories"])

@app.get("/")
async def root():
    return {"message": "RIWI - Sistema de Intervenciones de Couders API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "system": "RIWI Interventions", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
