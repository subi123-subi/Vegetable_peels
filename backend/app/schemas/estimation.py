from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


class EstimationInput(BaseModel):
    vegetable_id: Optional[int] = Field(None, description="Vegetable ID")
    vegetable_slug: Optional[str] = Field(None, description="Vegetable slug, e.g. 'carrot'")
    input_weight_grams: float = Field(..., gt=0, le=100000, description="Input weight in grams")
    input_weight_type: str = Field("peel", description="'peel' for direct peel weight, 'whole_vegetable' for unpeeled vegetable")
    vegetable_count: Optional[int] = Field(None, ge=1, le=50, description="Optional piece count (e.g. 2 potatoes)")
    preparation_method: str = Field("fresh_raw", description="fresh_raw, sauteed, boiled_broth, boiled_drained, dried_powder")
    population_group: str = Field("adult_male", description="adult_male, adult_female, pregnant_woman, lactating_mother, children_7_9y")
    servings: int = Field(1, ge=1, le=100, description="Number of consumer servings")


class PeelYieldRatioResponse(BaseModel):
    id: int
    vegetable_id: int
    vegetable_slug: str
    vegetable_name_en: str
    vegetable_name_ta: str
    average_peel_percentage: float
    min_peel_percentage: float
    max_peel_percentage: float
    moisture_percentage_fresh: float
    dry_matter_percentage: float
    water_loss_dehydration_factor: float
    pulp_comparison_notes_en: Optional[str] = None
    pulp_comparison_notes_ta: Optional[str] = None
    source_title: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class DailyReferenceIntakeResponse(BaseModel):
    id: int
    nutrient_code: str
    population_group: str
    rda_value: float
    unit: str
    standard_authority: str
    notes_en: Optional[str] = None
    notes_ta: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class NutrientIntakeDetail(BaseModel):
    nutrient_code: str
    nutrient_name_en: str
    nutrient_name_ta: str
    category: str  # vitamin, mineral, other
    concentration_per_100g_raw: float
    unit: str
    retention_factor: float
    estimated_amount: float
    estimated_amount_per_serving: float
    min_estimated_amount: Optional[float] = None
    max_estimated_amount: Optional[float] = None
    confidence_interval: Optional[str] = None
    rda_value: Optional[float] = None
    percentage_rda: Optional[float] = None
    rda_status: Optional[str] = None  # exceptional, good, moderate, trace
    rda_status_label_en: Optional[str] = None
    rda_status_label_ta: Optional[str] = None
    biological_role_en: Optional[str] = None
    biological_role_ta: Optional[str] = None


class EnvironmentalImpact(BaseModel):
    wet_waste_diverted_kg: float
    ghg_emissions_avoided_kg_co2e: float
    compost_potential_kg: float
    valorization_readiness: str


class NutritionalSuperiorityHighlight(BaseModel):
    comparison_en: str
    comparison_ta: str
    superior_nutrients: List[str] = []


class EstimationResponse(BaseModel):
    vegetable_id: int
    vegetable_slug: str
    vegetable_name_en: str
    vegetable_name_ta: str
    input_weight_grams: float
    input_weight_type: str
    calculated_peel_weight_grams: float
    peel_weight_range_grams: Dict[str, float]
    peel_yield_percentage: float
    dry_matter_weight_grams: float
    moisture_weight_grams: float
    preparation_method: str
    preparation_method_label_en: str
    preparation_method_label_ta: str
    population_group: str
    population_group_label_en: str
    population_group_label_ta: str
    servings: int
    nutrients: List[NutrientIntakeDetail]
    environmental_impact: EnvironmentalImpact
    superiority: NutritionalSuperiorityHighlight
    scientific_basis_notes: str
    timestamp: datetime


class SaveNutrientReportRequest(BaseModel):
    vegetable_id: int
    total_weight_grams: float
    calculations: Dict[str, Any]
    safety_notes: Optional[Dict[str, Any]] = None
    scan_id: Optional[int] = None
    user_feedback_notes: Optional[str] = None


class NutrientReportResponse(BaseModel):
    id: int
    report_uuid: str
    confirmation_id: Optional[int] = None
    total_weight_grams: Optional[float] = None
    calculations: Dict[str, Any]
    safety_notes: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
