# Import all the models, so that Base has them before being
# imported by Alembic or database initialization scripts
from app.db.base_class import Base  # noqa
from app.models.user import UserRole, User, AdminAuditLog  # noqa
from app.models.vegetable import PlantPart, Vegetable, VegetableAlias, VegetableImage  # noqa
from app.models.nutrient import ScientificSource, Nutrient, NutrientProfile, NutrientMeasurement, PeelYieldRatio, DailyReferenceIntake  # noqa
from app.models.safety import SafetyRule  # noqa
from app.models.reuse import ReuseMethod, ReuseRecommendation  # noqa
from app.models.scan import AIModelVersion, ScanRecord, ScanPrediction, UserConfirmation, NutrientReport, FeedbackRecord  # noqa
from app.models.translation import Translation  # noqa
from app.models.waste_tracking import WasteLog  # noqa

