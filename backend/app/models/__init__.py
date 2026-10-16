# Register all SQLAlchemy models in metadata registry
from app.models.user import UserRole, User, AdminAuditLog
from app.models.vegetable import PlantPart, Vegetable, VegetableAlias, VegetableImage
from app.models.nutrient import (
    ScientificSource,
    Nutrient,
    NutrientProfile,
    NutrientMeasurement,
    PeelYieldRatio,
    DailyReferenceIntake,
)
from app.models.safety import SafetyRule
from app.models.reuse import ReuseMethod, ReuseRecommendation
from app.models.scan import (
    AIModelVersion,
    ScanRecord,
    ScanPrediction,
    UserConfirmation,
    NutrientReport,
    FeedbackRecord,
)
from app.models.translation import Translation
from app.models.waste_tracking import WasteLog

__all__ = [
    "UserRole",
    "User",
    "AdminAuditLog",
    "PlantPart",
    "Vegetable",
    "VegetableAlias",
    "VegetableImage",
    "ScientificSource",
    "Nutrient",
    "NutrientProfile",
    "NutrientMeasurement",
    "PeelYieldRatio",
    "DailyReferenceIntake",
    "SafetyRule",
    "ReuseMethod",
    "ReuseRecommendation",
    "AIModelVersion",
    "ScanRecord",
    "ScanPrediction",
    "UserConfirmation",
    "NutrientReport",
    "FeedbackRecord",
    "Translation",
]
