from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .api import auth, couders, intervenciones, dashboard, ai, audio
from .core.database import engine
from .models import Base
from .middleware import LoggingMiddleware, SecurityMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clinical Intervention Tracking System",
    description="Sistema de registro individual de intervenciones clínicas",
    version="1.0.0"
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(SecurityMiddleware, calls_per_minute=100)
app.add_middleware(LoggingMiddleware)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(couders.router, prefix="/api/couders", tags=["couders"])
app.include_router(intervenciones.router, prefix="/api/intervenciones", tags=["intervenciones"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(audio.router, prefix="/api/audio", tags=["audio"])

@app.get("/")
async def root():
    return {"message": "Clinical Intervention Tracking System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
