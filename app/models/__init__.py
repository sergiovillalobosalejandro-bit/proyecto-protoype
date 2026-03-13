from ..core.database import Base

# New models based on real database structure
from .campus import Campus
from .cohort import Cohort, CohortStatus
from .clan import Clan, Shift
from .coder import Coder, CoderStatus
from .learning_path import LearningPath
from .specialist import Specialist
from .history import History
from .ai_report import AIReport

# Legacy models (keeping for compatibility)
# Temporarily disable all legacy models to avoid conflicts
# from .sedes import Sede
# from .cortes import Corte, TipoRuta
# from .clanes import LegacyClan, Jornada
# from .couders import Couder, EstadoCouder
# from .usuarios import Usuario, RolUsuario
# from .intervenciones import Intervencion

__all__ = [
    # New models
    "Base",
    "Campus",
    "Cohort", 
    "CohortStatus",
    "Clan",
    "Shift",
    "Coder",
    "CoderStatus",
    "LearningPath",
    "Specialist",
    "History",
    "AIReport",
    
    # Legacy models
    # "Sede",
    # "Corte", 
    # "TipoRuta",
    # "LegacyClan",
    # "Jornada",
    # "Couder",
    # "EstadoCouder",
    # "Usuario",
    # "RolUsuario",
    # "Intervencion"
]
