from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, utc_now


class AIModelVersion(Base):
    __tablename__ = "ai_model_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    version_tag: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)  # v1.0.0-mobilenetv3
    model_architecture: Mapped[str] = mapped_column(String(100), default="MobileNetV3Large")
    weights_file_path: Mapped[str] = mapped_column(String(300), nullable=False)
    input_shape: Mapped[str] = mapped_column(String(50), default="224,224,3")
    class_labels: Mapped[dict] = mapped_column(JSON, nullable=False)  # {"0": "carrot_peel", "1": "potato_peel", ...}
    accuracy: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    macro_f1: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active", index=True)  # active, candidate, deprecated
    trained_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    predictions: Mapped[List["ScanPrediction"]] = relationship("ScanPrediction", back_populates="model_version")


class ScanRecord(Base):
    __tablename__ = "scan_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    image_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, default=0)
    mime_type: Mapped[str] = mapped_column(String(50), default="image/jpeg")
    status: Mapped[str] = mapped_column(String(30), default="processed")  # uploaded, processed, confirmed, rejected
    scanned_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)

    user: Mapped[Optional["User"]] = relationship("User", back_populates="scans")
    predictions: Mapped[List["ScanPrediction"]] = relationship("ScanPrediction", back_populates="scan", cascade="all, delete-orphan")
    confirmation: Mapped[Optional["UserConfirmation"]] = relationship("UserConfirmation", back_populates="scan", uselist=False, cascade="all, delete-orphan")
    feedbacks: Mapped[List["FeedbackRecord"]] = relationship("FeedbackRecord", back_populates="scan")


class ScanPrediction(Base):
    __tablename__ = "scan_predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scan_id: Mapped[int] = mapped_column(Integer, ForeignKey("scan_records.id"), nullable=False, index=True)
    model_version_id: Mapped[int] = mapped_column(Integer, ForeignKey("ai_model_versions.id"), nullable=False, index=True)
    predicted_vegetable_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("vegetables.id"), nullable=True, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, default=1)  # 1 for top-1
    is_uncertain: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    scan: Mapped["ScanRecord"] = relationship("ScanRecord", back_populates="predictions")
    model_version: Mapped["AIModelVersion"] = relationship("AIModelVersion", back_populates="predictions")
    predicted_vegetable: Mapped[Optional["Vegetable"]] = relationship("Vegetable")


class UserConfirmation(Base):
    __tablename__ = "user_confirmations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scan_id: Mapped[int] = mapped_column(Integer, ForeignKey("scan_records.id"), nullable=False, unique=True, index=True)
    confirmed_vegetable_id: Mapped[int] = mapped_column(Integer, ForeignKey("vegetables.id"), nullable=False, index=True)
    confirmed_plant_part_id: Mapped[int] = mapped_column(Integer, ForeignKey("plant_parts.id"), nullable=False, index=True)
    confirmed_weight_grams: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_correction: Mapped[bool] = mapped_column(Boolean, default=False)
    user_feedback_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confirmed_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    scan: Mapped["ScanRecord"] = relationship("ScanRecord", back_populates="confirmation")
    confirmed_vegetable: Mapped["Vegetable"] = relationship("Vegetable")
    confirmed_plant_part: Mapped["PlantPart"] = relationship("PlantPart")
    nutrient_report: Mapped[Optional["NutrientReport"]] = relationship("NutrientReport", back_populates="confirmation", uselist=False, cascade="all, delete-orphan")


class NutrientReport(Base):
    __tablename__ = "nutrient_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    confirmation_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_confirmations.id"), nullable=False, unique=True, index=True)
    report_uuid: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    total_weight_grams: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    calculations: Mapped[dict] = mapped_column(JSON, nullable=False)
    safety_notes: Mapped[dict] = mapped_column(JSON, nullable=False)
    generated_pdf_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True)

    confirmation: Mapped["UserConfirmation"] = relationship("UserConfirmation", back_populates="nutrient_report")


class FeedbackRecord(Base):
    __tablename__ = "feedback_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    scan_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("scan_records.id"), nullable=True, index=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 to 5 stars
    feedback_type: Mapped[str] = mapped_column(String(50), default="accuracy")  # accuracy, safety, suggestion, bug
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    user: Mapped[Optional["User"]] = relationship("User", back_populates="feedbacks")
    scan: Mapped[Optional["ScanRecord"]] = relationship("ScanRecord", back_populates="feedbacks")
