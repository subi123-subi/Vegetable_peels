from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from app.db.session import get_db
from app.models.vegetable import Vegetable, PlantPart
from app.models.safety import SafetyRule
from app.models.reuse import ReuseRecommendation, ReuseMethod
from app.models.nutrient import NutrientProfile, NutrientMeasurement, Nutrient
from app.schemas.vegetable import (
    VegetableListResponse,
    VegetableDetailResponse,
    VegetableSummary,
    VegetableCreate,
    VegetableUpdate,
    PlantPartResponse,
    CategoryCountResponse,
    SafetyRuleBrief,
    NutrientMeasurementBrief,
    ReuseRecommendationBrief,
)

router = APIRouter()


@router.get("/", response_model=VegetableListResponse, summary="List Vegetables")
def list_vegetables(
    category: Optional[str] = Query(None, description="Filter by category (Root Vegetable, Gourds & Cucurbits, etc.)"),
    is_ai_supported: Optional[bool] = Query(None, description="Filter AI supported vegetables"),
    food_safety_status: Optional[str] = Query(None, description="Filter by safety classification"),
    plant_part_id: Optional[int] = Query(None, description="Filter by plant part ID"),
    search: Optional[str] = Query(None, description="Search by name in English, Tamil, scientific name, or slug"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page"),
    all: bool = Query(False, description="Return all active vegetables up to 200"),
    db: Session = Depends(get_db),
):
    query = db.query(Vegetable).options(joinedload(Vegetable.plant_part)).filter(Vegetable.is_active == True)

    if category and category.lower() != "all":
        query = query.filter(Vegetable.category.ilike(f"%{category}%"))

    if is_ai_supported is not None:
        query = query.filter(Vegetable.is_ai_supported == is_ai_supported)

    if food_safety_status:
        query = query.filter(Vegetable.food_safety_status == food_safety_status)

    if plant_part_id:
        query = query.filter(Vegetable.plant_part_id == plant_part_id)

    if search:
        search_filter = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Vegetable.name_en.ilike(search_filter),
                Vegetable.name_ta.ilike(search_filter),
                Vegetable.scientific_name.ilike(search_filter),
                Vegetable.slug.ilike(search_filter),
            )
        )

    total = query.count()

    if all:
        items = query.order_by(Vegetable.id.asc()).limit(200).all()
        page_size = len(items) if items else 50
    else:
        items = query.order_by(Vegetable.id.asc()).offset((page - 1) * page_size).limit(page_size).all()

    return VegetableListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[VegetableSummary.model_validate(v) for v in items],
    )


@router.get("/categories", response_model=List[CategoryCountResponse], summary="List Categories with Counts")
def list_categories(db: Session = Depends(get_db)):
    results = (
        db.query(Vegetable.category, func.count(Vegetable.id).label("count"))
        .filter(Vegetable.is_active == True)
        .group_by(Vegetable.category)
        .order_by(func.count(Vegetable.id).desc())
        .all()
    )
    return [CategoryCountResponse(category=r[0], count=r[1]) for r in results]


@router.get("/plant-parts", response_model=List[PlantPartResponse], summary="List Plant Parts")
def list_plant_parts(db: Session = Depends(get_db)):
    parts = db.query(PlantPart).order_by(PlantPart.id.asc()).all()
    return [PlantPartResponse.model_validate(p) for p in parts]


@router.get("/{id_or_slug}", response_model=VegetableDetailResponse, summary="Get Vegetable Detail")
def get_vegetable(
    id_or_slug: str,
    db: Session = Depends(get_db),
):
    query = db.query(Vegetable).options(
        joinedload(Vegetable.plant_part),
        joinedload(Vegetable.safety_rules),
        joinedload(Vegetable.reuse_recommendations).joinedload(ReuseRecommendation.reuse_method),
    )

    if id_or_slug.isdigit():
        veg = query.filter(Vegetable.id == int(id_or_slug)).first()
    else:
        veg = query.filter(Vegetable.slug == id_or_slug.strip().lower()).first()

    if not veg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vegetable '{id_or_slug}' not found in the catalogue.",
        )

    # Compile safety rules
    safety_rule_briefs = [
        SafetyRuleBrief(
            id=r.id,
            code=r.code,
            hazard_type=r.hazard_type,
            severity=r.severity,
            rule_description_en=r.rule_description_en,
            rule_description_ta=r.rule_description_ta,
            conservative_alternative_en=r.conservative_alternative_en,
            conservative_alternative_ta=r.conservative_alternative_ta,
        )
        for r in veg.safety_rules
    ]

    # Compile reuse recommendations
    reuse_briefs = [
        ReuseRecommendationBrief(
            id=rec.id,
            method_code=rec.reuse_method.code,
            method_name_en=rec.reuse_method.name_en,
            method_name_ta=rec.reuse_method.name_ta,
            category=rec.reuse_method.category,
            evidence_rank=rec.evidence_rank,
            preparation_instructions_en=rec.preparation_instructions_en,
            preparation_instructions_ta=rec.preparation_instructions_ta,
            limitations_and_warnings_en=rec.limitations_and_warnings_en,
            limitations_and_warnings_ta=rec.limitations_and_warnings_ta,
        )
        for rec in veg.reuse_recommendations
    ]

    # Compile measured nutrients from profiles
    nutrient_briefs: List[NutrientMeasurementBrief] = []
    profiles = (
        db.query(NutrientProfile)
        .options(
            joinedload(NutrientProfile.measurements).joinedload(NutrientMeasurement.nutrient),
        )
        .filter(NutrientProfile.vegetable_id == veg.id)
        .all()
    )

    for profile in profiles:
        for m in profile.measurements:
            nutrient_briefs.append(
                NutrientMeasurementBrief(
                    nutrient_id=m.nutrient.id,
                    nutrient_code=m.nutrient.code,
                    nutrient_name_en=m.nutrient.name_en,
                    nutrient_name_ta=m.nutrient.name_ta,
                    category=m.nutrient.category,
                    concentration_per_100g=m.concentration_per_100g,
                    unit=m.unit,
                    biological_role_en=m.nutrient.biological_role_en,
                    biological_role_ta=m.nutrient.biological_role_ta,
                    data_quality_status=profile.data_quality_status,
                )
            )

    detail_dict = {
        "id": veg.id,
        "slug": veg.slug,
        "name_en": veg.name_en,
        "name_ta": veg.name_ta,
        "scientific_name": veg.scientific_name,
        "category": veg.category,
        "plant_part_id": veg.plant_part_id,
        "plant_part": PlantPartResponse.model_validate(veg.plant_part) if veg.plant_part else None,
        "description_en": veg.description_en,
        "description_ta": veg.description_ta,
        "is_ai_supported": veg.is_ai_supported,
        "ai_class_name": veg.ai_class_name,
        "is_manually_selectable": veg.is_manually_selectable,
        "nutrient_data_status": veg.nutrient_data_status,
        "food_safety_status": veg.food_safety_status,
        "known_hazards_en": veg.known_hazards_en,
        "known_hazards_ta": veg.known_hazards_ta,
        "is_active": veg.is_active,
        "last_reviewed_at": veg.last_reviewed_at,
        "created_at": veg.created_at,
        "updated_at": veg.updated_at,
        "safety_rules": safety_rule_briefs,
        "nutrients": nutrient_briefs,
        "reuse_recommendations": reuse_briefs,
    }

    return VegetableDetailResponse(**detail_dict)


@router.post("/", response_model=VegetableSummary, status_code=status.HTTP_201_CREATED, summary="Create Vegetable")
def create_vegetable(
    payload: VegetableCreate,
    db: Session = Depends(get_db),
):
    # Check if slug already exists
    existing = db.query(Vegetable).filter(Vegetable.slug == payload.slug.strip().lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vegetable with slug '{payload.slug}' already exists in catalogue.",
        )

    # Check plant part
    plant_part = db.query(PlantPart).filter(PlantPart.id == payload.plant_part_id).first()
    if not plant_part:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Plant part ID {payload.plant_part_id} does not exist.",
        )

    new_veg = Vegetable(
        slug=payload.slug.strip().lower(),
        name_en=payload.name_en.strip(),
        name_ta=payload.name_ta.strip(),
        scientific_name=payload.scientific_name.strip(),
        category=payload.category.strip(),
        plant_part_id=payload.plant_part_id,
        description_en=payload.description_en,
        description_ta=payload.description_ta,
        is_ai_supported=payload.is_ai_supported,
        ai_class_name=payload.ai_class_name,
        is_manually_selectable=payload.is_manually_selectable,
        nutrient_data_status=payload.nutrient_data_status,
        food_safety_status=payload.food_safety_status,
        known_hazards_en=payload.known_hazards_en,
        known_hazards_ta=payload.known_hazards_ta,
        is_active=True,
    )
    db.add(new_veg)
    db.commit()
    db.refresh(new_veg)

    return VegetableSummary.model_validate(new_veg)


@router.put("/{id}", response_model=VegetableSummary, summary="Update Vegetable")
def update_vegetable(
    id: int,
    payload: VegetableUpdate,
    db: Session = Depends(get_db),
):
    veg = db.query(Vegetable).options(joinedload(Vegetable.plant_part)).filter(Vegetable.id == id).first()
    if not veg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vegetable with ID {id} not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)

    if "plant_part_id" in update_data and update_data["plant_part_id"] is not None:
        part = db.query(PlantPart).filter(PlantPart.id == update_data["plant_part_id"]).first()
        if not part:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Plant part ID {update_data['plant_part_id']} does not exist.",
            )

    for field, val in update_data.items():
        setattr(veg, field, val)

    db.commit()
    db.refresh(veg)

    return VegetableSummary.model_validate(veg)


@router.delete("/{id}", summary="Delete or Deactivate Vegetable")
def delete_vegetable(
    id: int,
    permanent: bool = Query(False, description="Permanently delete from database"),
    db: Session = Depends(get_db),
):
    veg = db.query(Vegetable).filter(Vegetable.id == id).first()
    if not veg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vegetable with ID {id} not found.",
        )

    if permanent:
        db.delete(veg)
    else:
        veg.is_active = False

    db.commit()
    return {"status": "success", "message": f"Vegetable ID {id} {'permanently deleted' if permanent else 'archived'}."}
