from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, utc_now


class ReuseMethod(Base):
    __tablename__ = "reuse_methods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)  # composting, vermicomposting, biogas, culinary_broth, pigment_extraction, animal_feed, bio_adsorbent
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    name_ta: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # food, composting, vermicomposting, biogas, animal_feed, pigment_extraction, bio_materials
    description_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description_ta: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    requires_special_processing: Mapped[bool] = mapped_column(Boolean, default=False)

    recommendations: Mapped[List["ReuseRecommendation"]] = relationship("ReuseRecommendation", back_populates="reuse_method")


class ReuseRecommendation(Base):
    __tablename__ = "reuse_recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vegetable_id: Mapped[int] = mapped_column(Integer, ForeignKey("vegetables.id"), nullable=False, index=True)
    plant_part_id: Mapped[int] = mapped_column(Integer, ForeignKey("plant_parts.id"), nullable=False, index=True)
    reuse_method_id: Mapped[int] = mapped_column(Integer, ForeignKey("reuse_methods.id"), nullable=False, index=True)
    evidence_rank: Mapped[int] = mapped_column(Integer, default=1, index=True)  # 1 (strongest) to 5

    preparation_instructions_en: Mapped[str] = mapped_column(Text, nullable=False)
    preparation_instructions_ta: Mapped[str] = mapped_column(Text, nullable=False)
    limitations_and_warnings_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    limitations_and_warnings_ta: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    reference_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("scientific_sources.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    vegetable: Mapped["Vegetable"] = relationship("Vegetable", back_populates="reuse_recommendations")
    plant_part: Mapped["PlantPart"] = relationship("PlantPart", back_populates="reuse_recommendations")
    reuse_method: Mapped["ReuseMethod"] = relationship("ReuseMethod", back_populates="recommendations")
    reference_source: Mapped[Optional["ScientificSource"]] = relationship("ScientificSource", back_populates="reuse_recommendations")
