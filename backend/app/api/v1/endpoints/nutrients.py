from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, func
from app.db.session import get_db
from app.models.nutrient import (
    Nutrient,
    NutrientProfile,
    NutrientMeasurement,
    ScientificSource,
    PeelYieldRatio,
    DailyReferenceIntake,
)
from app.models.vegetable import Vegetable, PlantPart
from app.models.scan import ScanRecord, UserConfirmation, NutrientReport
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
from app.schemas.estimation import (
    EstimationInput,
    EstimationResponse,
    PeelYieldRatioResponse,
    DailyReferenceIntakeResponse,
    SaveNutrientReportRequest,
    NutrientReportResponse,
)
from app.services.estimation_service import calculate_nutrient_estimation
from app.services.pdf_report_service import generate_nutrient_pdf
import uuid

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


# ==============================================================================
# PHASE 6 — NUTRITIONAL QUANTITY ESTIMATION ENGINE ENDPOINTS
# ==============================================================================

@router.post("/estimate", response_model=EstimationResponse, summary="Calculate Nutritional Quantity Estimation")
def estimate_nutrients(
    payload: EstimationInput,
    db: Session = Depends(get_db),
):
    """
    Scientifically estimates nutrient intake based on:
    - Input peel or whole vegetable weight
    - Botanical peel yield percentage and moisture/dry-matter composition
    - Preparation method thermal retention factors (fresh, sauteed, boiled, dried powder)
    - ICMR-NIN 2020 Recommended Dietary Allowance (% RDA) fulfillment
    - Food waste diversion and greenhouse gas mitigation potential
    """
    return calculate_nutrient_estimation(db=db, input_data=payload)


@router.get("/yield-ratios", response_model=List[PeelYieldRatioResponse], summary="List Vegetable Peel Yield Ratios")
def list_peel_yield_ratios(db: Session = Depends(get_db)):
    """Returns botanical peel yield ratios, moisture percentage, and dry matter for all catalogue vegetables."""
    ratios = (
        db.query(PeelYieldRatio)
        .options(joinedload(PeelYieldRatio.vegetable), joinedload(PeelYieldRatio.source))
        .join(Vegetable, PeelYieldRatio.vegetable_id == Vegetable.id)
        .order_by(Vegetable.id.asc())
        .all()
    )

    results = []
    for r in ratios:
        results.append(
            PeelYieldRatioResponse(
                id=r.id,
                vegetable_id=r.vegetable_id,
                vegetable_slug=r.vegetable.slug,
                vegetable_name_en=r.vegetable.name_en,
                vegetable_name_ta=r.vegetable.name_ta,
                average_peel_percentage=r.average_peel_percentage,
                min_peel_percentage=r.min_peel_percentage,
                max_peel_percentage=r.max_peel_percentage,
                moisture_percentage_fresh=r.moisture_percentage_fresh,
                dry_matter_percentage=r.dry_matter_percentage,
                water_loss_dehydration_factor=r.water_loss_dehydration_factor,
                pulp_comparison_notes_en=r.pulp_comparison_notes_en,
                pulp_comparison_notes_ta=r.pulp_comparison_notes_ta,
                source_title=r.source.title if r.source else None,
            )
        )
    return results


@router.get("/yield-ratios/{vegetable_slug}", response_model=PeelYieldRatioResponse, summary="Get Vegetable Peel Yield Ratio")
def get_peel_yield_ratio(vegetable_slug: str, db: Session = Depends(get_db)):
    """Returns botanical peel yield ratio for a specific vegetable by slug."""
    veg = db.query(Vegetable).filter(Vegetable.slug == vegetable_slug.strip().lower()).first()
    if not veg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vegetable '{vegetable_slug}' not found.",
        )

    ratio = (
        db.query(PeelYieldRatio)
        .options(joinedload(PeelYieldRatio.source))
        .filter(PeelYieldRatio.vegetable_id == veg.id)
        .first()
    )

    if not ratio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Peel yield ratio not recorded for '{vegetable_slug}'.",
        )

    return PeelYieldRatioResponse(
        id=ratio.id,
        vegetable_id=veg.id,
        vegetable_slug=veg.slug,
        vegetable_name_en=veg.name_en,
        vegetable_name_ta=veg.name_ta,
        average_peel_percentage=ratio.average_peel_percentage,
        min_peel_percentage=ratio.min_peel_percentage,
        max_peel_percentage=ratio.max_peel_percentage,
        moisture_percentage_fresh=ratio.moisture_percentage_fresh,
        dry_matter_percentage=ratio.dry_matter_percentage,
        water_loss_dehydration_factor=ratio.water_loss_dehydration_factor,
        pulp_comparison_notes_en=ratio.pulp_comparison_notes_en,
        pulp_comparison_notes_ta=ratio.pulp_comparison_notes_ta,
        source_title=ratio.source.title if ratio.source else None,
    )


@router.get("/dri", response_model=List[DailyReferenceIntakeResponse], summary="List Daily Reference Intakes (RDA)")
def list_daily_reference_intakes(
    population_group: Optional[str] = Query(None, description="Filter by demographic group (adult_male, adult_female, pregnant_woman, lactating_mother, children_7_9y)"),
    nutrient_code: Optional[str] = Query(None, description="Filter by nutrient code (e.g. vit_c, calcium)"),
    db: Session = Depends(get_db),
):
    """Returns ICMR-NIN 2020 Recommended Dietary Allowances."""
    query = db.query(DailyReferenceIntake)
    if population_group:
        query = query.filter(DailyReferenceIntake.population_group == population_group.strip().lower())
    if nutrient_code:
        query = query.filter(DailyReferenceIntake.nutrient_code == nutrient_code.strip().lower())

    records = query.order_by(DailyReferenceIntake.id.asc()).all()
    return [DailyReferenceIntakeResponse.model_validate(r) for r in records]


@router.post("/reports/save", response_model=NutrientReportResponse, status_code=status.HTTP_201_CREATED, summary="Save Nutrient Estimation Report")
def save_nutrient_report(
    payload: SaveNutrientReportRequest,
    db: Session = Depends(get_db),
):
    """Stores full nutrient intake calculation into reports archive."""
    veg = db.query(Vegetable).filter(Vegetable.id == payload.vegetable_id).first()
    if not veg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vegetable ID {payload.vegetable_id} not found.",
        )

    # Resolve or create confirmation
    plant_part = db.query(PlantPart).filter(PlantPart.code == "peel").first()
    plant_part_id = plant_part.id if plant_part else 1

    scan_id = payload.scan_id
    if not scan_id:
        # Create a virtual scan record for standalone report
        scan = ScanRecord(
            image_path=f"estimation://vegetable/{veg.slug}",
            file_size_bytes=0,
            mime_type="application/json",
            status="confirmed",
        )
        db.add(scan)
        db.flush()
        scan_id = scan.id

    confirmation = db.query(UserConfirmation).filter(UserConfirmation.scan_id == scan_id).first()
    if not confirmation:
        confirmation = UserConfirmation(
            scan_id=scan_id,
            confirmed_vegetable_id=veg.id,
            confirmed_plant_part_id=plant_part_id,
            confirmed_weight_grams=payload.total_weight_grams,
            user_feedback_notes=payload.user_feedback_notes,
        )
        db.add(confirmation)
        db.flush()

    report_uuid = f"RPT-{uuid.uuid4().hex[:12].upper()}"
    report = NutrientReport(
        confirmation_id=confirmation.id,
        report_uuid=report_uuid,
        total_weight_grams=payload.total_weight_grams,
        calculations=payload.calculations,
        safety_notes=payload.safety_notes or {"status": "evaluated", "hazards": []},
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return NutrientReportResponse(
        id=report.id,
        report_uuid=report.report_uuid,
        confirmation_id=report.confirmation_id,
        total_weight_grams=report.total_weight_grams,
        calculations=report.calculations,
        safety_notes=report.safety_notes,
        created_at=report.created_at,
    )


@router.get("/reports/{report_uuid}", response_model=NutrientReportResponse, summary="Get Saved Nutrient Report")
def get_nutrient_report(
    report_uuid: str,
    db: Session = Depends(get_db),
):
    """Retrieves an archived nutrient report by its unique UUID."""
    report = db.query(NutrientReport).filter(NutrientReport.report_uuid == report_uuid.strip()).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nutrient report '{report_uuid}' not found.",
        )
    return NutrientReportResponse(
        id=report.id,
        report_uuid=report.report_uuid,
        confirmation_id=report.confirmation_id,
        total_weight_grams=report.total_weight_grams,
        calculations=report.calculations,
        safety_notes=report.safety_notes,
        created_at=report.created_at,
    )


@router.get("/reports/{report_uuid}/pdf", summary="Download Nutrient Report PDF")
def download_nutrient_report_pdf(
    report_uuid: str,
    db: Session = Depends(get_db),
):
    """Generates and serves a publication-grade PDF report for an archived nutrient calculation."""
    report = db.query(NutrientReport).filter(NutrientReport.report_uuid == report_uuid.strip()).first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nutrient report '{report_uuid}' not found.",
        )
    calc_data = dict(report.calculations or {})
    calc_data["safety_notes"] = report.safety_notes
    calc_data["total_weight_grams"] = report.total_weight_grams
    pdf_bytes = generate_nutrient_pdf(calc_data, report_uuid=report.report_uuid)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=SmartPeel_Report_{report.report_uuid}.pdf"
        },
    )


@router.post("/reports/preview-pdf", summary="Generate On-The-Fly PDF from Estimation Input")
def preview_nutrient_estimation_pdf(
    payload: EstimationInput,
    db: Session = Depends(get_db),
):
    """Calculates nutrient estimations and returns an on-the-fly generated PDF report directly."""
    estimation = calculate_nutrient_estimation(db=db, input_data=payload)
    est_dict = estimation.model_dump()
    pdf_bytes = generate_nutrient_pdf(est_dict, report_uuid="RPT-ONTHEFLY")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=SmartPeel_Estimation_{payload.vegetable_slug}.pdf"
        },
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


