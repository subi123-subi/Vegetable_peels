from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, func
from app.db.session import get_db
from app.models.nutrient import Nutrient, NutrientProfile, NutrientMeasurement, ScientificSource
from app.models.vegetable import Vegetable, PlantPart
from app.schemas.nutrient import (
    NutrientResponse,
    NutrientCreate,
    NutrientMeasurementCreate,
    NutrientMeasurementDetail,
    NutrientProfileDetailResponse,
    ScientificSourceResponse,
    NutrientDetailWithTopSources,
    TopPeelSource,
)

router = APIRouter()


@router.get("/", response_model=List[NutrientResponse], summary="List Nutrients")
def list_nutrients(
    category: Optional[str] = Query(None, description="Filter by category (vitamin, mineral, other)"),
    db: Session = Depends(get_db),
):
    query = db.query(Nutrient)
    if category and category.lower() != "all":
        query = query.filter(Nutrient.category == category.lower())
    nutrients = query.order_by(Nutrient.id.asc()).all()
    return [NutrientResponse.model_validate(n) for n in nutrients]


@router.get("/categories", summary="List Nutrient Categories")
def list_nutrient_categories(db: Session = Depends(get_db)):
    results = (
        db.query(Nutrient.category, func.count(Nutrient.id).label("count"))
        .group_by(Nutrient.category)
        .order_by(func.count(Nutrient.id).desc())
        .all()
    )
    return [{"category": r[0], "count": r[1]} for r in results]


@router.get("/sources", response_model=List[ScientificSourceResponse], summary="List Scientific Sources")
def list_sources(db: Session = Depends(get_db)):
    sources = db.query(ScientificSource).order_by(ScientificSource.id.asc()).all()
    return [ScientificSourceResponse.model_validate(s) for s in sources]


@router.get("/profiles/{vegetable_slug}", response_model=NutrientProfileDetailResponse, summary="Get Vegetable Nutrient Profile")
def get_vegetable_nutrient_profile(
    vegetable_slug: str,
    db: Session = Depends(get_db),
):
    veg = db.query(Vegetable).filter(Vegetable.slug == vegetable_slug.strip().lower()).first()
    if not veg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vegetable '{vegetable_slug}' not found.",
        )

    profile = (
        db.query(NutrientProfile)
        .options(
            joinedload(NutrientProfile.source),
            joinedload(NutrientProfile.plant_part),
            joinedload(NutrientProfile.measurements).joinedload(NutrientMeasurement.nutrient),
        )
        .filter(NutrientProfile.vegetable_id == veg.id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No scientific nutrient profile recorded for '{vegetable_slug}'.",
        )

    meas_details = []
    for m in profile.measurements:
        meas_details.append(
            NutrientMeasurementDetail(
                id=m.id,
                nutrient_id=m.nutrient.id,
                nutrient_code=m.nutrient.code,
                nutrient_name_en=m.nutrient.name_en,
                nutrient_name_ta=m.nutrient.name_ta,
                category=m.nutrient.category,
                concentration_per_100g=m.concentration_per_100g,
                unit=m.unit,
                measurement_method=m.measurement_method,
                min_value=m.min_value,
                max_value=m.max_value,
                confidence_interval=m.confidence_interval,
                biological_role_en=m.nutrient.biological_role_en,
                biological_role_ta=m.nutrient.biological_role_ta,
            )
        )

    return NutrientProfileDetailResponse(
        id=profile.id,
        vegetable_id=veg.id,
        vegetable_slug=veg.slug,
        vegetable_name_en=veg.name_en,
        vegetable_name_ta=veg.name_ta,
        plant_part_id=profile.plant_part_id,
        plant_part_code=profile.plant_part.code if profile.plant_part else "peel",
        fresh_or_dry_basis=profile.fresh_or_dry_basis,
        sample_prep_method=profile.sample_prep_method,
        uncertainty_notes=profile.uncertainty_notes,
        data_quality_status=profile.data_quality_status,
        source=ScientificSourceResponse.model_validate(profile.source) if profile.source else None,
        measurements=meas_details,
        created_at=profile.created_at,
    )


@router.get("/{code_or_id}", response_model=NutrientDetailWithTopSources, summary="Get Nutrient Detail with Top Peel Sources")
def get_nutrient_detail(
    code_or_id: str,
    db: Session = Depends(get_db),
):
    if code_or_id.isdigit():
        nutrient = db.query(Nutrient).filter(Nutrient.id == int(code_or_id)).first()
    else:
        nutrient = db.query(Nutrient).filter(Nutrient.code == code_or_id.strip().lower()).first()

    if not nutrient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nutrient '{code_or_id}' not found.",
        )

    # Find top vegetable peel sources for this nutrient
    measurements = (
        db.query(NutrientMeasurement)
        .options(
            joinedload(NutrientMeasurement.profile).joinedload(NutrientProfile.vegetable),
        )
        .filter(NutrientMeasurement.nutrient_id == nutrient.id)
        .order_by(desc(NutrientMeasurement.concentration_per_100g))
        .limit(10)
        .all()
    )

    top_sources = []
    for m in measurements:
        if m.profile and m.profile.vegetable:
            top_sources.append(
                TopPeelSource(
                    vegetable_id=m.profile.vegetable.id,
                    vegetable_slug=m.profile.vegetable.slug,
                    vegetable_name_en=m.profile.vegetable.name_en,
                    vegetable_name_ta=m.profile.vegetable.name_ta,
                    concentration_per_100g=m.concentration_per_100g,
                    unit=m.unit,
                    data_quality_status=m.profile.data_quality_status,
                )
            )

    nutrient_data = NutrientResponse.model_validate(nutrient).model_dump()
    nutrient_data["top_peel_sources"] = top_sources
    return NutrientDetailWithTopSources(**nutrient_data)


@router.post("/", response_model=NutrientResponse, status_code=status.HTTP_201_CREATED, summary="Create Nutrient Definition")
def create_nutrient(
    payload: NutrientCreate,
    db: Session = Depends(get_db),
):
    existing = db.query(Nutrient).filter(Nutrient.code == payload.code.strip().lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nutrient with code '{payload.code}' already exists.",
        )

    new_n = Nutrient(
        code=payload.code.strip().lower(),
        name_en=payload.name_en.strip(),
        name_ta=payload.name_ta.strip(),
        category=payload.category.strip().lower(),
        standard_unit=payload.standard_unit.strip(),
        description_en=payload.description_en,
        description_ta=payload.description_ta,
        biological_role_en=payload.biological_role_en,
        biological_role_ta=payload.biological_role_ta,
    )
    db.add(new_n)
    db.commit()
    db.refresh(new_n)
    return NutrientResponse.model_validate(new_n)


@router.post("/measurements", status_code=status.HTTP_201_CREATED, summary="Add Nutrient Measurement")
def add_measurement(
    payload: NutrientMeasurementCreate,
    db: Session = Depends(get_db),
):
    profile = db.query(NutrientProfile).filter(NutrientProfile.id == payload.profile_id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nutrient profile ID {payload.profile_id} does not exist.",
        )

    nut = db.query(Nutrient).filter(Nutrient.id == payload.nutrient_id).first()
    if not nut:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nutrient ID {payload.nutrient_id} does not exist.",
        )

    meas = NutrientMeasurement(
        profile_id=payload.profile_id,
        nutrient_id=payload.nutrient_id,
        concentration_per_100g=payload.concentration_per_100g,
        unit=payload.unit,
        measurement_method=payload.measurement_method,
        min_value=payload.min_value,
        max_value=payload.max_value,
        confidence_interval=payload.confidence_interval,
    )
    db.add(meas)
    db.commit()
    db.refresh(meas)
    return {"status": "success", "measurement_id": meas.id}
