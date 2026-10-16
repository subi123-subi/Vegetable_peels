from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.safety import SafetyRule
from app.models.vegetable import Vegetable
from app.schemas.safety import (
    SafetyEvaluationRequest,
    SafetyEvaluationResponse,
    SafetyRuleDetail,
)
from app.services.safety_service import evaluate_peel_safety

router = APIRouter()


@router.post(
    "/evaluate",
    response_model=SafetyEvaluationResponse,
    status_code=status.HTTP_200_OK,
    summary="Evaluate vegetable peel food safety & biological hazards",
)
def evaluate_safety(
    payload: SafetyEvaluationRequest,
    db: Session = Depends(get_db),
):
    """
    Evaluates known botanical hazards (glycoalkaloids, cyanogenic glucosides, oxalate raphides,
    cucurbitacins, pesticide residues) and dynamic user conditions (sprouting, greening, mould, bitterness).
    Enforces scientific food safety rules before allowing culinary valorization recommendations.
    """
    try:
        response = evaluate_peel_safety(
            db=db,
            vegetable_slug=payload.vegetable_slug,
            conditions=payload.conditions,
            scan_confidence=payload.scan_confidence,
        )
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/rules",
    response_model=List[SafetyRuleDetail],
    summary="List all biological and chemical food safety rules",
)
def list_safety_rules(
    severity: Optional[str] = Query(None, description="Filter by severity: critical, warning, notice"),
    hazard_type: Optional[str] = Query(None, description="Filter by hazard type"),
    db: Session = Depends(get_db),
):
    query = db.query(SafetyRule)
    if severity:
        query = query.filter(SafetyRule.severity == severity.lower())
    if hazard_type:
        query = query.filter(SafetyRule.hazard_type == hazard_type.lower())

    rules = query.order_by(SafetyRule.id.asc()).all()
    results = []
    for r in rules:
        ref_text = (
            f"{r.reference_source.title} ({r.reference_source.publication_year or ''})"
            if r.reference_source
            else "ICMR-NIN / FAO Food Safety Guidelines"
        )
        results.append(
            SafetyRuleDetail(
                id=r.id,
                code=r.code,
                hazard_type=r.hazard_type,
                severity=r.severity,
                rule_description_en=r.rule_description_en,
                rule_description_ta=r.rule_description_ta,
                scientific_reference=ref_text,
                conservative_alternative_en=r.conservative_alternative_en,
                conservative_alternative_ta=r.conservative_alternative_ta,
            )
        )
    return results


@router.get(
    "/rules/{code}",
    response_model=SafetyRuleDetail,
    summary="Get details of a specific safety rule by code",
)
def get_safety_rule(code: str, db: Session = Depends(get_db)):
    rule = db.query(SafetyRule).filter(SafetyRule.code == code.strip().upper()).first()
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Safety rule '{code}' not found.",
        )

    ref_text = (
        f"{rule.reference_source.title} ({rule.reference_source.publication_year or ''})"
        if rule.reference_source
        else "ICMR-NIN / FAO Food Safety Guidelines"
    )
    return SafetyRuleDetail(
        id=rule.id,
        code=rule.code,
        hazard_type=rule.hazard_type,
        severity=rule.severity,
        rule_description_en=rule.rule_description_en,
        rule_description_ta=rule.rule_description_ta,
        scientific_reference=ref_text,
        conservative_alternative_en=rule.conservative_alternative_en,
        conservative_alternative_ta=rule.conservative_alternative_ta,
    )
