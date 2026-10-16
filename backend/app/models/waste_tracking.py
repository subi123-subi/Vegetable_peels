from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, utc_now


class WasteLog(Base):
    __tablename__ = "waste_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    scan_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("scan_records.id"), nullable=True, index=True)
    vegetable_id: Mapped[int] = mapped_column(Integer, ForeignKey("vegetables.id"), nullable=False, index=True)
    plant_part_id: Mapped[int] = mapped_column(Integer, ForeignKey("plant_parts.id"), nullable=False, index=True)
    reuse_method_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("reuse_methods.id"), nullable=True, index=True)

    weight_grams: Mapped[float] = mapped_column(Float, nullable=False)
    is_diverted: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    diversion_category: Mapped[str] = mapped_column(String(50), default="composting", index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    logged_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)

    vegetable: Mapped["Vegetable"] = relationship("Vegetable")
    plant_part: Mapped["PlantPart"] = relationship("PlantPart")
    reuse_method: Mapped[Optional["ReuseMethod"]] = relationship("ReuseMethod")
