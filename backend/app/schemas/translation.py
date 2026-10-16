from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class TranslationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    translation_key: str
    language_code: str
    translated_text: str
    context: Optional[str] = None
    created_at: datetime


class TranslationCreate(BaseModel):
    translation_key: str = Field(..., min_length=2, max_length=150)
    language_code: str = Field(..., pattern="^(en|ta)$")
    translated_text: str = Field(..., min_length=1)
    context: Optional[str] = Field("ui", max_length=100)


class TranslationDictionary(BaseModel):
    language_code: str
    translations: Dict[str, str]
