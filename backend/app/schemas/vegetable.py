from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class PlantPartResponse(BaseModel):
    id: int
    code: str
    name_en: str
    name_ta: str
    description_en: Optional[str] = None
    description_ta: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VegetableBase(BaseModel):
    slug: str
    name_en: str
    name_ta: str
    scientific_name: str
    category: str
    description_en: Optional[str] = None
    description_ta: Optional[str] = None
    is_ai_supported: bool = False
    ai_class_name: Optional[str] = None
    is_manually_selectable: bool = True
    nutrient_data_status: str = "incomplete"  # 'available', 'incomplete', 'reference_only'
    food_safety_status: str = "conditional_cooking_required"  # 'safe_edible', 'conditional_cooking_required', 'hazardous_raw', 'inedible_valorize_only'
    known_hazards_en: Optional[str] = None
    known_hazards_ta: Optional[str] = None
    is_active: bool = True


class VegetableCreate(BaseModel):
    slug: str = Field(..., min_length=2, max_length=100)
    name_en: str = Field(..., min_length=2, max_length=120)
    name_ta: str = Field(..., min_length=2, max_length=120)
    scientific_name: str = Field(..., min_length=2, max_length=150)
    category: str = Field(..., min_length=2, max_length=100)
    plant_part_id: int
    description_en: Optional[str] = None
    description_ta: Optional[str] = None
    is_ai_supported: bool = False
    ai_class_name: Optional[str] = None
    is_manually_selectable: bool = True
    nutrient_data_status: str = "incomplete"
    food_safety_status: str = "conditional_cooking_required"
    known_hazards_en: Optional[str] = None
    known_hazards_ta: Optional[str] = None


class VegetableUpdate(BaseModel):
    name_en: Optional[str] = None
    name_ta: Optional[str] = None
    scientific_name: Optional[str] = None
    category: Optional[str] = None
    plant_part_id: Optional[int] = None
    description_en: Optional[str] = None
    description_ta: Optional[str] = None
    is_ai_supported: Optional[bool] = None
    ai_class_name: Optional[str] = None
    is_manually_selectable: Optional[bool] = None
    nutrient_data_status: Optional[str] = None
    food_safety_status: Optional[str] = None
    known_hazards_en: Optional[str] = None
    known_hazards_ta: Optional[str] = None
    is_active: Optional[bool] = None


class VegetableSummary(BaseModel):
    id: int
    slug: str
    name_en: str
    name_ta: str
    scientific_name: str
    category: str
    is_ai_supported: bool
    ai_class_name: Optional[str] = None
    nutrient_data_status: str
    food_safety_status: str
    known_hazards_en: Optional[str] = None
    known_hazards_ta: Optional[str] = None
    plant_part_id: int
    plant_part: Optional[PlantPartResponse] = None

    model_config = ConfigDict(from_attributes=True)


class SafetyRuleBrief(BaseModel):
    id: int
    code: str
    hazard_type: str
    severity: str
    rule_description_en: str
    rule_description_ta: str
    conservative_alternative_en: Optional[str] = None
    conservative_alternative_ta: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class NutrientMeasurementBrief(BaseModel):
    nutrient_id: int
    nutrient_code: str
    nutrient_name_en: str
    nutrient_name_ta: str
    category: str
    concentration_per_100g: float
    unit: str
    biological_role_en: Optional[str] = None
    biological_role_ta: Optional[str] = None
    data_quality_status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ReuseRecommendationBrief(BaseModel):
    id: int
    method_code: str
    method_name_en: str
    method_name_ta: str
    category: str
    evidence_rank: int
    preparation_instructions_en: str
    preparation_instructions_ta: str
    limitations_and_warnings_en: Optional[str] = None
    limitations_and_warnings_ta: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VegetableDetail(VegetableBase):
    id: int
    plant_part_id: int
    plant_part: Optional[PlantPartResponse] = None
    last_reviewed_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VegetableDetailResponse(VegetableDetail):
    safety_rules: List[SafetyRuleBrief] = []
    nutrients: List[NutrientMeasurementBrief] = []
    reuse_recommendations: List[ReuseRecommendationBrief] = []


class VegetableListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[VegetableSummary]


class CategoryCountResponse(BaseModel):
    category: str
    count: int
