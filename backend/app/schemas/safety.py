from typing import Optional, List
from pydantic import BaseModel, Field


class SafetyConditionFlags(BaseModel):
    is_green_or_sprouted: bool = Field(False, description="Presence of green skin/flesh or eye sprouts (solanine risk)")
    is_bitter_tasting: bool = Field(False, description="Unusual bitter taste in gourds/cucurbits (cucurbitacin toxicity)")
    has_visible_mould: bool = Field(False, description="Fungal growth or black/grey/green spores (mycotoxin risk)")
    is_unwashed: bool = Field(True, description="Unwashed produce fresh from market (pesticide/microbial risk)")


class SafetyEvaluationRequest(BaseModel):
    vegetable_slug: str = Field(..., description="Slug of the vegetable being evaluated")
    conditions: SafetyConditionFlags = Field(default_factory=SafetyConditionFlags)
    scan_confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="AI classification confidence score")


class SafetyRuleDetail(BaseModel):
    id: int
    code: str
    hazard_type: str
    severity: str  # critical, warning, notice
    rule_description_en: str
    rule_description_ta: str
    scientific_reference: Optional[str] = None
    conservative_alternative_en: Optional[str] = None
    conservative_alternative_ta: Optional[str] = None


class ConservativeAlternative(BaseModel):
    method_code: str
    name_en: str
    name_ta: str
    category: str  # composting, biogas, vermicompost, etc.
    description_en: str
    description_ta: str


class SafetyEvaluationResponse(BaseModel):
    vegetable_slug: str
    vegetable_name_en: str
    vegetable_name_ta: str
    scientific_name: str
    intrinsic_safety_status: str
    overall_safety_status: str  # safe_edible, conditional_cooking_required, hazardous_raw, inedible_valorize_only, critical_hazard_discard
    edible_recommendation_allowed: bool
    is_hazardous: bool
    requires_special_processing: bool
    processing_instructions_en: Optional[str] = None
    processing_instructions_ta: Optional[str] = None
    active_hazards: List[SafetyRuleDetail]
    conservative_alternatives: List[ConservativeAlternative]
    general_safety_disclaimer_en: str
    general_safety_disclaimer_ta: str
