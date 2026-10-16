from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.db.session import get_db
from app.models.reuse import ReuseMethod, ReuseRecommendation
from app.models.vegetable import Vegetable
from app.schemas.reuse import (
    ReuseMethodResponse,
    ReuseRecommendationItem,
    WasteValorizationResponse,
)

router = APIRouter()


@router.get(
    "/methods",
    response_model=List[ReuseMethodResponse],
    summary="List all supported waste valorization methods",
)
def list_reuse_methods(
    category: Optional[str] = Query(None, description="Filter by category (food, composting, biogas, etc.)"),
    db: Session = Depends(get_db),
):
    query = db.query(ReuseMethod)
    if category and category.lower() != "all":
        query = query.filter(ReuseMethod.category == category.lower())
    methods = query.order_by(ReuseMethod.id.asc()).all()
    return [ReuseMethodResponse.model_validate(m) for m in methods]


@router.get(
    "/categories",
    summary="List all valorization categories with method counts",
)
def list_reuse_categories(db: Session = Depends(get_db)):
    results = (
        db.query(ReuseMethod.category, func.count(ReuseMethod.id).label("count"))
        .group_by(ReuseMethod.category)
        .order_by(func.count(ReuseMethod.id).desc())
        .all()
    )
    return [{"category": r[0], "count": r[1]} for r in results]


@router.get(
    "/recommendations/{vegetable_slug}",
    response_model=WasteValorizationResponse,
    summary="Retrieve evidence-ranked reuse recommendations for a vegetable",
)
def get_vegetable_reuse_recommendations(
    vegetable_slug: str,
    include_experimental: bool = Query(True, description="Include laboratory / experimental methods"),
    db: Session = Depends(get_db),
):
    """
    Retrieves evidence-ranked valorization methods (culinary, composting, vermicomposting,
    biogas, natural pigments, bio-materials) for confirmed vegetable peel material.
    Strictly filters out culinary recommendations if the vegetable is marked as hazardous or inedible.
    """
    veg = db.query(Vegetable).filter(Vegetable.slug == vegetable_slug.strip().lower()).first()
    if not veg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vegetable '{vegetable_slug}' not found.",
        )

    # Food safety enforcement:
    is_food_safe = veg.food_safety_status in ["safe_edible", "conditional_cooking_required"]

    query = (
        db.query(ReuseRecommendation)
        .options(
            joinedload(ReuseRecommendation.reuse_method),
            joinedload(ReuseRecommendation.plant_part),
            joinedload(ReuseRecommendation.reference_source),
        )
        .filter(ReuseRecommendation.vegetable_id == veg.id)
    )

    if not include_experimental:
        query = query.filter(ReuseRecommendation.evidence_rank <= 3)

    recs = query.order_by(ReuseRecommendation.evidence_rank.asc()).all()

    items: List[ReuseRecommendationItem] = []
    for r in recs:
        # Strictly inhibit culinary food recommendations if vegetable is hazardous or inedible
        if r.reuse_method.category == "food" and not is_food_safe:
            continue

        ref_str = (
            f"{r.reference_source.title} ({r.reference_source.publication_year or ''})"
            if r.reference_source
            else "FAO / ICAR Valorization Best Practices"
        )

        items.append(
            ReuseRecommendationItem(
                id=r.id,
                method_code=r.reuse_method.code,
                method_name_en=r.reuse_method.name_en,
                method_name_ta=r.reuse_method.name_ta,
                category=r.reuse_method.category,
                evidence_rank=r.evidence_rank,
                preparation_instructions_en=r.preparation_instructions_en,
                preparation_instructions_ta=r.preparation_instructions_ta,
                limitations_and_warnings_en=r.limitations_and_warnings_en,
                limitations_and_warnings_ta=r.limitations_and_warnings_ta,
                reference_citation=ref_str,
                is_food_safe=r.reuse_method.category == "food" and is_food_safe,
            )
        )

    return WasteValorizationResponse(
        vegetable_id=veg.id,
        vegetable_slug=veg.slug,
        vegetable_name_en=veg.name_en,
        vegetable_name_ta=veg.name_ta,
        scientific_name=veg.scientific_name,
        plant_part=veg.plant_part.name_en if veg.plant_part else "Peel",
        food_safety_status=veg.food_safety_status,
        edible_culinary_allowed=is_food_safe,
        total_recommendations=len(items),
        recommendations=items,
    )
