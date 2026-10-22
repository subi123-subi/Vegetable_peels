from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class PredictionItem(BaseModel):
    class_key: str
    slug: str
    confidence: float
    display_name_en: str
    display_name_ta: str
    scientific_name: str
    is_supported_peel: bool


class ScanPredictResponse(BaseModel):
    scan_id: int
    prediction_id: int
    predicted_vegetable_slug: Optional[str] = None
    predicted_display_name_en: str
    predicted_display_name_ta: str
    predicted_plant_part: str = "Peel / தோல்"
    confidence: float
    model_version: str
    is_supported_peel: bool
    confirmation_required: bool
    is_uncertain: bool
    top_predictions: List[PredictionItem]
    safety_notice: str
    scanned_at: datetime
    is_mixture: Optional[bool] = False
    mixture_components: Optional[List[dict]] = None


class UserConfirmationCreate(BaseModel):
    scan_id: int
    confirmed_vegetable_id: int
    confirmed_plant_part_id: Optional[int] = None
    confirmed_weight_grams: Optional[float] = Field(None, gt=0, le=10000)
    is_correction: bool = False
    user_feedback_notes: Optional[str] = None


class UserConfirmationResponse(BaseModel):
    id: int
    scan_id: int
    confirmed_vegetable_id: int
    confirmed_vegetable_name_en: str
    confirmed_vegetable_name_ta: str
    confirmed_weight_grams: Optional[float]
    is_correction: bool
    confirmed_at: datetime


class ModelInfoResponse(BaseModel):
    version_tag: str
    architecture: str
    classes_count: int
    confidence_threshold: float
    accuracy: Optional[float]
    macro_f1: Optional[float]
    classes: List[dict]


class DetectedWasteItem(BaseModel):
    vegetable_id: int
    slug: str
    name_en: str
    name_ta: str
    scientific_name: str
    category: str
    plant_part: str
    confidence: float
    share_percentage: float
    food_safety_status: str
    known_hazards_en: Optional[str] = None
    known_hazards_ta: Optional[str] = None
    safety_rules: List[str] = []
    top_nutrients: List[dict] = []
    best_reuse_method: str = "Composting"


class MixtureSafetyAssessment(BaseModel):
    overall_status: str
    title_en: str
    title_ta: str
    summary_en: str
    summary_ta: str
    critical_warnings: List[str] = []


class CompositeNutrientItem(BaseModel):
    name_en: str
    name_ta: str
    category: str
    unit: str
    estimated_amount_per_100g: float


class MixtureValorizationRecommendation(BaseModel):
    method_name_en: str
    method_name_ta: str
    category: str
    suitability_rating: str
    instructions_en: str
    instructions_ta: str
    limitations_en: Optional[str] = None


class MixedPeelAnalysisResponse(BaseModel):
    is_mixture: bool = True
    mixture_title_en: str
    mixture_title_ta: str
    total_detected_components: int
    detected_wastes: List[DetectedWasteItem]
    safety_assessment: MixtureSafetyAssessment
    composite_nutrients: List[CompositeNutrientItem]
    recommended_valorization: MixtureValorizationRecommendation

