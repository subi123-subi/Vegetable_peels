from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base, utc_now


class Translation(Base):
    __tablename__ = "translations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    translation_key: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    language_code: Mapped[str] = mapped_column(String(10), nullable=False, index=True)  # 'en', 'ta'
    translated_text: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # ui, error, safety, nutrient
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)

    __table_args__ = (
        UniqueConstraint("translation_key", "language_code", name="uq_translation_key_lang"),
    )
