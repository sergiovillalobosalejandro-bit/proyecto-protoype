# Temporarily disable legacy APIs to avoid conflicts
# from . import auth, couders, intervenciones, dashboard, ai, audio
from . import campus, cohorts, clans, coders, specialists, histories

__all__ = [
    # "auth", 
    # "couders", 
    # "intervenciones", 
    # "dashboard", 
    # "ai", 
    # "audio",
    "campus", 
    "cohorts",
    "clans",
    "coders", 
    "specialists",
    "histories"
]