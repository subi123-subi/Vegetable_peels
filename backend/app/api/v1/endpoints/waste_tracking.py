from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc

from app.db.session import get_db
from app.models.waste_tracking import WasteLog
from app.models.vegetable import Vegetable, PlantPart
from app.models.reuse import ReuseMethod
from app.schemas.waste_tracking import (
    WasteLogCreate,
    WasteLogResponse,
    WasteSummaryResponse,
    CategoryBreakdownItem,
    TimePeriodTotalItem,
)

router = APIRouter()


@router.post(
    "/log",
    response_model=WasteLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record a peel waste generation or diversion event",
)
def create_waste_log(
    payload: WasteLogCreate,
    db: Session = Depends(get_db),
):
    """
    Logs vegetable peel waste weight and tracks whether it was diverted via
    composting, vermiculture, biogas, or culinary use vs discarded to landfill.
    """
    veg = db.query(Vegetable).filter(Vegetable.slug == payload.vegetable_slug.strip().lower()).first()
    if not veg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vegetable '{payload.vegetable_slug}' not found.",
        )

    plant_part = db.query(PlantPart).filter(PlantPart.code == payload.plant_part_code.strip().lower()).first()
    if not plant_part:
        plant_part = db.query(PlantPart).first()

    reuse_method = None
    diversion_category = "landfill_disposal"
    if payload.reuse_method_code:
        reuse_method = db.query(ReuseMethod).filter(ReuseMethod.code == payload.reuse_method_code.strip().lower()).first()
        if reuse_method:
            diversion_category = reuse_method.category

    # If user explicitly marked not diverted, override category
    if not payload.is_diverted:
        diversion_category = "landfill_disposal"

    log_entry = WasteLog(
        vegetable_id=veg.id,
        plant_part_id=plant_part.id,
        reuse_method_id=reuse_method.id if reuse_method else None,
        weight_grams=payload.weight_grams,
        is_diverted=payload.is_diverted,
        diversion_category=diversion_category,
        notes=payload.notes,
        logged_at=payload.logged_at or datetime.utcnow(),
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    return WasteLogResponse(
        id=log_entry.id,
        vegetable_id=veg.id,
        vegetable_slug=veg.slug,
        vegetable_name_en=veg.name_en,
        vegetable_name_ta=veg.name_ta,
        weight_grams=log_entry.weight_grams,
        weight_kg=round(log_entry.weight_grams / 1000.0, 3),
        is_diverted=log_entry.is_diverted,
        diversion_category=log_entry.diversion_category,
        reuse_method_code=reuse_method.code if reuse_method else None,
        reuse_method_name_en=reuse_method.name_en if reuse_method else None,
        reuse_method_name_ta=reuse_method.name_ta if reuse_method else None,
        notes=log_entry.notes,
        logged_at=log_entry.logged_at,
    )


@router.get(
    "/logs",
    response_model=List[WasteLogResponse],
    summary="List chronological waste tracking logs",
)
def list_waste_logs(
    is_diverted: Optional[bool] = Query(None, description="Filter by diversion status"),
    vegetable_slug: Optional[str] = Query(None, description="Filter by vegetable slug"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = (
        db.query(WasteLog)
        .options(
            joinedload(WasteLog.vegetable),
            joinedload(WasteLog.reuse_method),
        )
    )

    if is_diverted is not None:
        query = query.filter(WasteLog.is_diverted == is_diverted)
    if vegetable_slug:
        query = query.join(Vegetable).filter(Vegetable.slug == vegetable_slug.strip().lower())

    logs = query.order_by(desc(WasteLog.logged_at)).offset(offset).limit(limit).all()

    results = []
    for log in logs:
        results.append(
            WasteLogResponse(
                id=log.id,
                vegetable_id=log.vegetable.id,
                vegetable_slug=log.vegetable.slug,
                vegetable_name_en=log.vegetable.name_en,
                vegetable_name_ta=log.vegetable.name_ta,
                weight_grams=log.weight_grams,
                weight_kg=round(log.weight_grams / 1000.0, 3),
                is_diverted=log.is_diverted,
                diversion_category=log.diversion_category,
                reuse_method_code=log.reuse_method.code if log.reuse_method else None,
                reuse_method_name_en=log.reuse_method.name_en if log.reuse_method else None,
                reuse_method_name_ta=log.reuse_method.name_ta if log.reuse_method else None,
                notes=log.notes,
                logged_at=log.logged_at,
            )
        )
    return results


@router.get(
    "/summary",
    response_model=WasteSummaryResponse,
    summary="Aggregated smart waste tracking dashboard and diversion trends",
)
def get_waste_summary(db: Session = Depends(get_db)):
    """
    Computes total recorded waste, total diverted waste, percentage diversion rate,
    breakdown by valorization method, and daily/weekly/monthly trends.
    """
    logs = db.query(WasteLog).order_by(WasteLog.logged_at.asc()).all()

    total_weight_grams = sum(l.weight_grams for l in logs)
    diverted_weight_grams = sum(l.weight_grams for l in logs if l.is_diverted)

    total_kg = round(total_weight_grams / 1000.0, 3)
    diverted_kg = round(diverted_weight_grams / 1000.0, 3)
    diversion_rate = round((diverted_weight_grams / total_weight_grams * 100.0), 1) if total_weight_grams > 0 else 0.0

    # Category Breakdown
    cat_map = {}
    for l in logs:
        cat = l.diversion_category
        cat_map.setdefault(cat, {"grams": 0.0, "count": 0})
        cat_map[cat]["grams"] += l.weight_grams
        cat_map[cat]["count"] += 1

    by_category = []
    for cat, val in cat_map.items():
        cat_kg = round(val["grams"] / 1000.0, 3)
        pct = round((val["grams"] / total_weight_grams * 100.0), 1) if total_weight_grams > 0 else 0.0
        by_category.append(
            CategoryBreakdownItem(
                category=cat,
                weight_kg=cat_kg,
                percentage=pct,
                count=val["count"],
            )
        )

    # Daily Totals
    daily_map = {}
    weekly_map = {}
    monthly_map = {}

    for l in logs:
        day_str = l.logged_at.strftime("%Y-%m-%d")
        week_str = l.logged_at.strftime("%Y-W%W")
        month_str = l.logged_at.strftime("%Y-%m")

        for key, m in [(day_str, daily_map), (week_str, weekly_map), (month_str, monthly_map)]:
            m.setdefault(key, {"total": 0.0, "diverted": 0.0})
            m[key]["total"] += l.weight_grams
            if l.is_diverted:
                m[key]["diverted"] += l.weight_grams

    def format_periods(p_map):
        res = []
        for p, d in sorted(p_map.items()):
            tot_k = round(d["total"] / 1000.0, 3)
            div_k = round(d["diverted"] / 1000.0, 3)
            r = round((d["diverted"] / d["total"] * 100.0), 1) if d["total"] > 0 else 0.0
            res.append(
                TimePeriodTotalItem(
                    period=p,
                    total_waste_kg=tot_k,
                    diverted_waste_kg=div_k,
                    diversion_rate=r,
                )
            )
        return res

    return WasteSummaryResponse(
        total_recorded_waste_kg=total_kg,
        total_diverted_waste_kg=diverted_kg,
        diversion_rate_percentage=diversion_rate,
        total_logs_count=len(logs),
        by_category=sorted(by_category, key=lambda x: x.weight_kg, reverse=True),
        daily_totals=format_periods(daily_map),
        weekly_totals=format_periods(weekly_map),
        monthly_totals=format_periods(monthly_map),
    )


@router.delete(
    "/logs/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a waste tracking log entry",
)
def delete_waste_log(log_id: int, db: Session = Depends(get_db)):
    entry = db.get(WasteLog, log_id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log entry not found.")
    db.delete(entry)
    db.commit()
    return None
