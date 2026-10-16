from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class ScientificSourceResponse(BaseModel):
    id: int
    title: str
    authors: Optional[str] = None
    publication_year: Optional[int] = None
    journal_or_publisher: Optional[str] = None
    doi_or_url: Optional[str] = None
    source_type: str
    reliability_rating: str

    model_config = ConfigDict(from_attributes=True)


class NutrientBase(BaseModel):
    code: str
    name_en: str
    name_ta: str
    category: str  # vitamin, mineral, other
    standard_unit: str  # mg, mcg, g
    description_en: Optional[str] = None
    description_ta: Optional[str] = None
    biological_role_en: Optional[str] = None
    biological_role_ta: Optional[str] = None


class NutrientCreate(NutrientBase):
    pass


class NutrientResponse(NutrientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class NutrientMeasurementCreate(BaseModel):
    profile_id: int
    nutrient_id: int
    concentration_per_100g: float
    unit: str
    measurement_method: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    confidence_interval: Optional[str] = None


class NutrientMeasurementDetail(BaseModel):
    id: int
    nutrient_id: int
    nutrient_code: str
    nutrient_name_en: str
    nutrient_name_ta: str
    category: str
    concentration_per_100g: float
    unit: str
    measurement_method: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    confidence_interval: Optional[str] = None
    biological_role_en: Optional[str] = None
    biological_role_ta: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class NutrientProfileDetailResponse(BaseModel):
    id: int
    vegetable_id: int
    vegetable_slug: str
    vegetable_name_en: str
    vegetable_name_ta: str
    plant_part_id: int
    plant_part_code: str
    fresh_or_dry_basis: str
    sample_prep_method: Optional[str] = None
    uncertainty_notes: Optional[str] = None
    data_quality_status: str
    source: Optional[ScientificSourceResponse] = None
    measurements: List[NutrientMeasurementDetail] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TopPeelSource(BaseModel):
    vegetable_id: int
    vegetable_slug: str
    vegetable_name_en: str
    vegetable_name_ta: str
    concentration_per_100g: float
    unit: str
    data_quality_status: str


class NutrientDetailWithTopSources(NutrientResponse):
    top_peel_sources: List[TopPeelSource] = []
