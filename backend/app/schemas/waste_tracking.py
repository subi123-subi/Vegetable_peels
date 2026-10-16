from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class WasteLogCreate(BaseModel):
    vegetable_slug: str = Field(..., description="Slug of the vegetable")
    plant_part_code: str = Field("peel", description="Plant part code: peel, skin, rind")
    weight_grams: float = Field(..., gt=0, le=50000, description="Weight in grams (up to 50kg)")
    reuse_method_code: Optional[str] = Field(None, description="Reuse method code (e.g. aerobic_composting, biogas_anaerobic, culinary_stock)")
    is_diverted: bool = Field(True, description="Whether the waste was diverted from landfill disposal")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes or observations")
    logged_at: Optional[datetime] = Field(None, description="Event timestamp (defaults to current time)")


class WasteLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    vegetable_id: int
    vegetable_slug: str
    vegetable_name_en: str
    vegetable_name_ta: str
    weight_grams: float
    weight_kg: float
    is_diverted: bool
    diversion_category: str
    reuse_method_code: Optional[str] = None
    reuse_method_name_en: Optional[str] = None
    reuse_method_name_ta: Optional[str] = None
    notes: Optional[str] = None
    logged_at: datetime


class CategoryBreakdownItem(BaseModel):
    category: str
    weight_kg: float
    percentage: float
    count: int


class TimePeriodTotalItem(BaseModel):
    period: str  # e.g., '2026-10-16' or '2026-W42' or '2026-10'
    total_waste_kg: float
    diverted_waste_kg: float
    diversion_rate: float


class WasteSummaryResponse(BaseModel):
    total_recorded_waste_kg: float
    total_diverted_waste_kg: float
    diversion_rate_percentage: float
    total_logs_count: int
    by_category: List[CategoryBreakdownItem]
    daily_totals: List[TimePeriodTotalItem]
    weekly_totals: List[TimePeriodTotalItem]
    monthly_totals: List[TimePeriodTotalItem]
