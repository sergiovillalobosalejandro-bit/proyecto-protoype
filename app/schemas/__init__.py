# New schemas based on real database structure
from .campus import CampusCreate, CampusResponse, CampusUpdate
from .cohort import CohortCreate, CohortResponse, CohortUpdate
from .clan import ClanCreate, ClanResponse, ClanUpdate, ClanWithCoders
from .coder import CoderCreate, CoderResponse, CoderUpdate, CoderWithDetails, CoderSimpleResponse
from .specialist import SpecialistCreate, SpecialistResponse, SpecialistUpdate
from .history import HistoryCreate, HistoryResponse, HistoryUpdate
from .ai_report import AIReportCreate, AIReportResponse, AIReportUpdate
from .learning_path import LearningPathCreate, LearningPathResponse, LearningPathUpdate

# Legacy schemas temporarily disabled
# from .auth import UserCreate, UserResponse, Token, TokenData
# from .couders import CouderBase, CouderCreate, CouderUpdate, CouderResponse, CouderWithDetails
# from .intervenciones import IntervencionBase, IntervencionCreate, IntervencionUpdate, IntervencionResponse, ClinicalHistoryRecord
# from .dashboard import AudioRecordBase, AudioRecordCreate, AudioRecordResponse

__all__ = [
    # New schemas
    "CampusCreate", "CampusResponse", "CampusUpdate",
    "CohortCreate", "CohortResponse", "CohortUpdate",
    "ClanCreate", "ClanResponse", "ClanUpdate", "ClanWithCoders",
    "CoderCreate", "CoderResponse", "CoderUpdate", "CoderWithDetails", "CoderSimpleResponse",
    "SpecialistCreate", "SpecialistResponse", "SpecialistUpdate",
    "HistoryCreate", "HistoryResponse", "HistoryUpdate",
    "AIReportCreate", "AIReportResponse", "AIReportUpdate",
    "LearningPathCreate", "LearningPathResponse", "LearningPathUpdate",
]