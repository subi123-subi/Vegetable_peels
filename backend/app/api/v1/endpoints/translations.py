from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.translation import Translation
from app.schemas.translation import (
    TranslationResponse,
    TranslationCreate,
    TranslationDictionary,
)

router = APIRouter()

SEED_TRANSLATIONS = [
    # Navigation & General
    {"key": "app_name", "lang": "en", "text": "SMART PEEL AI", "context": "ui"},
    {"key": "app_name", "lang": "ta", "text": "ஸ்மார்ட் பீல் ஏஐ", "context": "ui"},
    {"key": "tagline", "lang": "en", "text": "Intelligent Vegetable Peel Nutrient Identification & Valorization System", "context": "ui"},
    {"key": "tagline", "lang": "ta", "text": "காய்கறி தோல் ஊட்டச்சத்து கண்டறிதல் மற்றும் மறுபயன்பாட்டு முறைமை", "context": "ui"},
    {"key": "home", "lang": "en", "text": "Home", "context": "ui"},
    {"key": "home", "lang": "ta", "text": "முகப்பு", "context": "ui"},
    {"key": "scan_peel", "lang": "en", "text": "Scan Peel", "context": "ui"},
    {"key": "scan_peel", "lang": "ta", "text": "தோல் ஸ்கேன்", "context": "ui"},
    {"key": "vegetable_catalogue", "lang": "en", "text": "Vegetables Catalogue", "context": "ui"},
    {"key": "vegetable_catalogue", "lang": "ta", "text": "காய்கறி பட்டியல்", "context": "ui"},
    {"key": "history", "lang": "en", "text": "Scan History", "context": "ui"},
    {"key": "history", "lang": "ta", "text": "ஸ்கேன் வரலாறு", "context": "ui"},
    {"key": "waste_tracking", "lang": "en", "text": "Waste Diversion Tracker", "context": "ui"},
    {"key": "waste_tracking", "lang": "ta", "text": "கழிவு கண்காணிப்பான்", "context": "ui"},
    {"key": "profile", "lang": "en", "text": "My Profile", "context": "ui"},
    {"key": "profile", "lang": "ta", "text": "சுயவிவரம்", "context": "ui"},
    {"key": "settings", "lang": "en", "text": "Settings", "context": "ui"},
    {"key": "settings", "lang": "ta", "text": "அமைப்புகள்", "context": "ui"},
    {"key": "admin_console", "lang": "en", "text": "Administrator Console", "context": "ui"},
    {"key": "admin_console", "lang": "ta", "text": "நிர்வாக கட்டுப்பாட்டு பலகை", "context": "ui"},

    # Scientific Disclaimers & Safety
    {"key": "scientific_disclaimer", "lang": "en", "text": "Nutrient estimates are derived from verified scientific databases (ICMR-NIN IFCT 2017 & USDA FDC), representing statistical expectations rather than direct laboratory assays of your individual sample.", "context": "safety"},
    {"key": "scientific_disclaimer", "lang": "ta", "text": "ஊட்டச்சத்து மதிப்பீடுகள் சரிபார்க்கப்பட்ட அறிவியல் குறிப்புகளை (ICMR-NIN & USDA) அடிப்படையாகக் கொண்டவை; இது உங்கள் தனிப்பட்ட மாதிரியின் நேரடி ஆய்வக அளவீடு அல்ல.", "context": "safety"},
    {"key": "solanine_warning", "lang": "en", "text": "Green or sprouted potato peels contain solanine glycoalkaloid toxins. Discard entirely — unsafe for cooking or livestock.", "context": "safety"},
    {"key": "solanine_warning", "lang": "ta", "text": "பச்சை அல்லது முளைத்த உருளைக்கிழங்கு தோல்களில் சோலனைன் நச்சு உள்ளது. உணவிற்கோ கால்நடைகளுக்கோ பயன்படுத்தாமல் அப்புறப்படுத்தவும்.", "context": "safety"},
    {"key": "cyanide_warning", "lang": "en", "text": "Cassava / tapioca peel contains toxic cyanogenic glucosides. Must never be consumed raw or cooked for food.", "context": "safety"},
    {"key": "cyanide_warning", "lang": "ta", "text": "மரவள்ளிக்கிழங்கு தோலில் சயனோஜெனிக் நச்சு உள்ளது. இதை ஒருபோதும் சமையல் உணவாக உட்கொள்ளக்கூடாது.", "context": "safety"},
    {"key": "oxalate_warning", "lang": "en", "text": "Taro and colocasia peels contain calcium oxalate raphide crystals causing severe throat irritation unless thoroughly cooked.", "context": "safety"},
    {"key": "oxalate_warning", "lang": "ta", "text": "சேப்பங்கிழங்கு தோலில் கால்சியம் ஆக்சலேட் படிகங்கள் உள்ளதால், நன்கு வேகவைக்காமல் உட்கொண்டால் தொண்டை அரிப்பு ஏற்படும்.", "context": "safety"},

    # Valorization Methods
    {"key": "composting", "lang": "en", "text": "Aerobic Composting", "context": "reuse"},
    {"key": "composting", "lang": "ta", "text": "காற்றுள்ள மட்கச் செய்தல்", "context": "reuse"},
    {"key": "vermicomposting", "lang": "en", "text": "Vermicomposting", "context": "reuse"},
    {"key": "vermicomposting", "lang": "ta", "text": "மண்புழு உரம் தயாரிப்பு", "context": "reuse"},
    {"key": "biogas", "lang": "en", "text": "Anaerobic Biogas Digestion", "context": "reuse"},
    {"key": "biogas", "lang": "ta", "text": "உயிரி எரிவாயு உற்பத்தி", "context": "reuse"},
    {"key": "culinary_broth", "lang": "en", "text": "Culinary Broth / Chips", "context": "reuse"},
    {"key": "culinary_broth", "lang": "ta", "text": "சமையல் சூப் / வறுவல்", "context": "reuse"},
    {"key": "animal_feed", "lang": "en", "text": "Livestock Feed Supplement", "context": "reuse"},
    {"key": "animal_feed", "lang": "ta", "text": "கால்நடை தீவன துணைப்பொருள்", "context": "reuse"},
]


@router.get("/dictionary", response_model=TranslationDictionary)
def get_translation_dictionary(
    lang: str = Query("en", pattern="^(en|ta)$"),
    context: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Retrieve full key-value translation dictionary for client UI binding."""
    query = db.query(Translation).filter(Translation.language_code == lang)
    if context:
        query = query.filter(Translation.context == context)

    entries = query.all()
    trans_map = {e.translation_key: e.translated_text for e in entries}

    # Fallback to seeded in-memory dictionary if DB is missing keys
    for item in SEED_TRANSLATIONS:
        if item["lang"] == lang and (not context or item["context"] == context):
            if item["key"] not in trans_map:
                trans_map[item["key"]] = item["text"]

    return TranslationDictionary(
        language_code=lang,
        translations=trans_map,
    )


@router.get("/", response_model=List[TranslationResponse])
def list_translations(
    lang: Optional[str] = Query(None, pattern="^(en|ta)$"),
    context: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Retrieve detailed translations list."""
    query = db.query(Translation)
    if lang:
        query = query.filter(Translation.language_code == lang)
    if context:
        query = query.filter(Translation.context == context)

    return query.order_by(Translation.translation_key).all()


@router.post("/", response_model=TranslationResponse, status_code=status.HTTP_201_CREATED)
def create_or_update_translation(
    payload: TranslationCreate,
    db: Session = Depends(get_db),
):
    """Create or update a localized string entry."""
    existing = (
        db.query(Translation)
        .filter(
            Translation.translation_key == payload.translation_key,
            Translation.language_code == payload.language_code,
        )
        .first()
    )

    if existing:
        existing.translated_text = payload.translated_text
        if payload.context:
            existing.context = payload.context
        db.commit()
        db.refresh(existing)
        return existing

    new_trans = Translation(
        translation_key=payload.translation_key,
        language_code=payload.language_code,
        translated_text=payload.translated_text,
        context=payload.context,
    )
    db.add(new_trans)
    db.commit()
    db.refresh(new_trans)
    return new_trans


@router.post("/seed", status_code=status.HTTP_200_OK)
def seed_translations_database(db: Session = Depends(get_db)):
    """Seed comprehensive English & Tamil translations into the database."""
    seeded_count = 0
    for item in SEED_TRANSLATIONS:
        existing = (
            db.query(Translation)
            .filter(
                Translation.translation_key == item["key"],
                Translation.language_code == item["lang"],
            )
            .first()
        )
        if not existing:
            new_record = Translation(
                translation_key=item["key"],
                language_code=item["lang"],
                translated_text=item["text"],
                context=item["context"],
            )
            db.add(new_record)
            seeded_count += 1

    db.commit()
    return {
        "status": "success",
        "message": f"Successfully seeded {seeded_count} bilingual translation records.",
        "total_available": len(SEED_TRANSLATIONS),
    }
