from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, utc_now

if TYPE_CHECKING:
    from app.models.vegetable import Vegetable
    from app.models.nutrient import ScientificSource


class SafetyRule(Base):
    __tablename__ = "safety_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    vegetable_id: Mapped[int] = mapped_column(Integer, ForeignKey("vegetables.id"), nullable=False, index=True)
    hazard_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # glycoalkaloid, cyanogenic_glucoside, oxalate_raphide, cucurbitacin, pesticide_residue
    severity: Mapped[str] = mapped_column(String(20), default="warning", index=True)  # critical, warning, notice

    rule_description_en: Mapped[str] = mapped_column(Text, nullable=False)
    rule_description_ta: Mapped[str] = mapped_column(Text, nullable=False)

    scientific_reference_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("scientific_sources.id"), nullable=True)
    conservative_alternative_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    conservative_alternative_ta: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    vegetable: Mapped["Vegetable"] = relationship("Vegetable", back_populates="safety_rules")
    reference_source: Mapped[Optional["ScientificSource"]] = relationship("ScientificSource", back_populates="safety_rules")
