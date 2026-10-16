from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, utc_now


class PlantPart(Base):
    __tablename__ = "plant_parts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)  # peel, skin, rind, husk, outer_leaves, pod_shell, stem_layer
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    name_ta: Mapped[str] = mapped_column(String(100), nullable=False)
    description_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description_ta: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    vegetables: Mapped[List["Vegetable"]] = relationship("Vegetable", back_populates="plant_part")
    nutrient_profiles: Mapped[List["NutrientProfile"]] = relationship("NutrientProfile", back_populates="plant_part")
    reuse_recommendations: Mapped[List["ReuseRecommendation"]] = relationship("ReuseRecommendation", back_populates="plant_part")


class Vegetable(Base):
    __tablename__ = "vegetables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name_en: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    name_ta: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    scientific_name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # Root, Gourd, Common, Bulb, Outer Layer
    plant_part_id: Mapped[int] = mapped_column(Integer, ForeignKey("plant_parts.id"), nullable=False, index=True)

    description_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description_ta: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    is_ai_supported: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    ai_class_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    is_manually_selectable: Mapped[bool] = mapped_column(Boolean, default=True)

    # Data & safety statuses
    nutrient_data_status: Mapped[str] = mapped_column(String(50), default="incomplete")  # 'available', 'incomplete', 'unavailable'
    food_safety_status: Mapped[str] = mapped_column(String(50), default="conditional_cooking_required")  # 'safe_edible', 'conditional_cooking_required', 'hazardous_raw', 'inedible_valorize_only'

    known_hazards_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    known_hazards_ta: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    last_reviewed_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)

    plant_part: Mapped["PlantPart"] = relationship("PlantPart", back_populates="vegetables")
    aliases: Mapped[List["VegetableAlias"]] = relationship("VegetableAlias", back_populates="vegetable", cascade="all, delete-orphan")
    images: Mapped[List["VegetableImage"]] = relationship("VegetableImage", back_populates="vegetable", cascade="all, delete-orphan")
    nutrient_profiles: Mapped[List["NutrientProfile"]] = relationship("NutrientProfile", back_populates="vegetable", cascade="all, delete-orphan")
    peel_yield_ratio: Mapped[Optional["PeelYieldRatio"]] = relationship("PeelYieldRatio", back_populates="vegetable", uselist=False, cascade="all, delete-orphan")
    safety_rules: Mapped[List["SafetyRule"]] = relationship("SafetyRule", back_populates="vegetable", cascade="all, delete-orphan")
    reuse_recommendations: Mapped[List["ReuseRecommendation"]] = relationship("ReuseRecommendation", back_populates="vegetable", cascade="all, delete-orphan")



class VegetableAlias(Base):
    __tablename__ = "vegetable_aliases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vegetable_id: Mapped[int] = mapped_column(Integer, ForeignKey("vegetables.id"), nullable=False, index=True)
    alias_name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    language: Mapped[str] = mapped_column(String(10), default="en")

    vegetable: Mapped["Vegetable"] = relationship("Vegetable", back_populates="aliases")


class VegetableImage(Base):
    __tablename__ = "vegetable_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    vegetable_id: Mapped[int] = mapped_column(Integer, ForeignKey("vegetables.id"), nullable=False, index=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    caption: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    vegetable: Mapped["Vegetable"] = relationship("Vegetable", back_populates="images")
