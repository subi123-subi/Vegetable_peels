from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class PlantPartResponse(BaseModel):
    id: int
    code: str
    name_en: str
    name_ta: str

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
    nutrient_data_status: str
    food_safety_status: str
    known_hazards_en: Optional[str] = None
    known_hazards_ta: Optional[str] = None
    is_active: bool = True


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
    plant_part: Optional[PlantPartResponse] = None

    model_config = ConfigDict(from_attributes=True)


class VegetableDetail(VegetableBase):
    id: int
    plant_part_id: int
    plant_part: Optional[PlantPartResponse] = None
    last_reviewed_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VegetableListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[VegetableSummary]
