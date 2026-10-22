from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class ReuseMethodResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name_en: str
    name_ta: str
    category: str
    description_en: Optional[str] = None
    description_ta: Optional[str] = None
    requires_special_processing: bool


class ReuseRecommendationItem(BaseModel):
    id: int
    method_code: str
    method_name_en: str
    method_name_ta: str
    category: str
    evidence_rank: int  # 1 to 5 (1 is highest evidence)
    preparation_instructions_en: str
    preparation_instructions_ta: str
    limitations_and_warnings_en: Optional[str] = None
    limitations_and_warnings_ta: Optional[str] = None
    reference_citation: Optional[str] = None
    is_food_safe: bool


class WasteValorizationResponse(BaseModel):
    vegetable_id: int
    vegetable_slug: str
    vegetable_name_en: str
    vegetable_name_ta: str
    scientific_name: str
    plant_part: str
    food_safety_status: str
    edible_culinary_allowed: bool
    total_recommendations: int
    recommendations: List[ReuseRecommendationItem]


class WasteCreationItem(BaseModel):
    id: str
    title_en: str
    title_ta: str
    category: str  # garden_soil, eco_home, culinary_gourmet, arts_crafts, natural_wellness
    category_name_en: str
    category_name_ta: str
    suitable_peels: List[str]
    difficulty: str  # Easy, Moderate, Ferment
    prep_time_minutes: int
    total_time: str
    estimated_output: str
    icon_name: str
    impact_summary_en: str
    impact_summary_ta: str
    required_materials_en: List[str]
    required_materials_ta: List[str]
    step_by_step_instructions_en: List[str]
    step_by_step_instructions_ta: List[str]
    safety_and_storage_en: str
    safety_and_storage_ta: str
    scientific_rationale_en: str
    scientific_rationale_ta: str


class WasteCreationsListResponse(BaseModel):
    total: int
    categories: List[str]
    creations: List[WasteCreationItem]
