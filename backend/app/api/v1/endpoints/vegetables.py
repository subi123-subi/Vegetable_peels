from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.db.session import get_db
from app.models.vegetable import Vegetable
from app.schemas.vegetable import VegetableListResponse, VegetableDetail, VegetableSummary

router = APIRouter()


@router.get("/", response_model=VegetableListResponse, summary="List Vegetables")
def list_vegetables(
    category: Optional[str] = Query(None, description="Filter by category (Root, Gourd, etc.)"),
    is_ai_supported: Optional[bool] = Query(None, description="Filter AI supported vegetables"),
    search: Optional[str] = Query(None, description="Search by name in English or Tamil or scientific name"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
):
    query = db.query(Vegetable).options(joinedload(Vegetable.plant_part)).filter(Vegetable.is_active == True)

    if category:
        query = query.filter(Vegetable.category.ilike(f"%{category}%"))

    if is_ai_supported is not None:
        query = query.filter(Vegetable.is_ai_supported == is_ai_supported)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Vegetable.name_en.ilike(search_filter),
                Vegetable.name_ta.ilike(search_filter),
                Vegetable.scientific_name.ilike(search_filter),
                Vegetable.slug.ilike(search_filter),
            )
        )

    total = query.count()
    items = query.order_by(Vegetable.id.asc()).offset((page - 1) * page_size).limit(page_size).all()

    return VegetableListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[VegetableSummary.model_validate(v) for v in items],
    )


@router.get("/{id_or_slug}", response_model=VegetableDetail, summary="Get Vegetable Detail")
def get_vegetable(
    id_or_slug: str,
    db: Session = Depends(get_db),
):
    query = db.query(Vegetable).options(joinedload(Vegetable.plant_part))
    if id_or_slug.isdigit():
        veg = query.filter(Vegetable.id == int(id_or_slug)).first()
    else:
        veg = query.filter(Vegetable.slug == id_or_slug).first()

    if not veg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vegetable '{id_or_slug}' not found in the catalogue.",
        )
    return VegetableDetail.model_validate(veg)
