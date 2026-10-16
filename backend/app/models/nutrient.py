from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, utc_now


class ScientificSource(Base):
    __tablename__ = "scientific_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    authors: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    publication_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    journal_or_publisher: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    doi_or_url: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    source_type: Mapped[str] = mapped_column(String(50), default="peer_reviewed")  # icmr_nin, usda, peer_reviewed, institutional
    reliability_rating: Mapped[str] = mapped_column(String(20), default="high")  # high, moderate, preliminary
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    nutrient_profiles: Mapped[List["NutrientProfile"]] = relationship("NutrientProfile", back_populates="source")
    safety_rules: Mapped[List["SafetyRule"]] = relationship("SafetyRule", back_populates="reference_source")
    reuse_recommendations: Mapped[List["ReuseRecommendation"]] = relationship("ReuseRecommendation", back_populates="reference_source")


class Nutrient(Base):
    __tablename__ = "nutrients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)  # vit_c, calcium, dietary_fibre, etc.
    name_en: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name_ta: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # vitamin, mineral, other
    standard_unit: Mapped[str] = mapped_column(String(20), nullable=False)  # mg, mcg, g
    description_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description_ta: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    biological_role_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    biological_role_ta: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    measurements: Mapped[List["NutrientMeasurement"]] = relationship("NutrientMeasurement", back_populates="nutrient")


class NutrientProfile(Base):
    __tablename__ = "nutrient_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vegetable_id: Mapped[int] = mapped_column(Integer, ForeignKey("vegetables.id"), nullable=False, index=True)
    plant_part_id: Mapped[int] = mapped_column(Integer, ForeignKey("plant_parts.id"), nullable=False, index=True)
    source_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("scientific_sources.id"), nullable=True, index=True)

    fresh_or_dry_basis: Mapped[str] = mapped_column(String(20), default="fresh_weight")  # fresh_weight, dry_weight
    sample_prep_method: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    uncertainty_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data_quality_status: Mapped[str] = mapped_column(String(50), default="validated_peel_measurement")  # validated_peel_measurement, indicative_estimate, whole_vegetable_context_only
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    vegetable: Mapped["Vegetable"] = relationship("Vegetable", back_populates="nutrient_profiles")
    plant_part: Mapped["PlantPart"] = relationship("PlantPart", back_populates="nutrient_profiles")
    source: Mapped[Optional["ScientificSource"]] = relationship("ScientificSource", back_populates="nutrient_profiles")
    measurements: Mapped[List["NutrientMeasurement"]] = relationship("NutrientMeasurement", back_populates="profile", cascade="all, delete-orphan")


class NutrientMeasurement(Base):
    __tablename__ = "nutrient_measurements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("nutrient_profiles.id"), nullable=False, index=True)
    nutrient_id: Mapped[int] = mapped_column(Integer, ForeignKey("nutrients.id"), nullable=False, index=True)
    concentration_per_100g: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    measurement_method: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    min_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    confidence_interval: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    profile: Mapped["NutrientProfile"] = relationship("NutrientProfile", back_populates="measurements")
    nutrient: Mapped["Nutrient"] = relationship("Nutrient", back_populates="measurements")
