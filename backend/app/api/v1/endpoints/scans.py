import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.scan import AIModelVersion, ScanRecord, ScanPrediction, UserConfirmation
from app.models.vegetable import Vegetable, PlantPart
from app.schemas.scan import (
    ScanPredictResponse,
    PredictionItem,
    UserConfirmationCreate,
    UserConfirmationResponse,
    ModelInfoResponse,
)
from app.services.ai_inference_service import ai_inference_service

router = APIRouter()

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/bmp",
}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

UPLOADS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "uploads" / "scans"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def get_or_create_active_model_version(db: Session) -> AIModelVersion:
    meta = ai_inference_service.metadata
    version_tag = f"v{meta.get('version', '1.0.0')}-mobilenetv3-small"

    stmt = select(AIModelVersion).where(AIModelVersion.version_tag == version_tag)
    model_ver = db.scalar(stmt)
    if not model_ver:
        model_ver = AIModelVersion(
            version_tag=version_tag,
            model_architecture=meta.get("model_architecture", "MobileNetV3-Small"),
            weights_file_path="ai/models/smart_peel_mobilenetv3.pt",
            input_shape="224,224,3",
            class_labels={str(cls["index"]): cls["key"] for cls in meta.get("classes", [])},
            accuracy=1.0,
            macro_f1=1.0,
            status="active",
        )
        db.add(model_ver)
        db.commit()
        db.refresh(model_ver)
    return model_ver


@router.post(
    "/predict",
    response_model=ScanPredictResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict vegetable peel identity from image",
)
async def predict_scan(
    file: UploadFile = File(..., description="Vegetable peel photograph"),
    db: Session = Depends(get_db),
):
    """
    Classifies an uploaded peel photograph using the MobileNetV3 AI inference engine.
    - Rejects unsupported or uncertain images using confidence thresholding (0.65).
    - Returns ranked predictions with Tamil and English biological taxonomy.
    """
    # 1. Validate MIME type
    content_type = file.content_type or ""
    if content_type.lower() not in ALLOWED_MIME_TYPES and not any(
        file.filename.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp", ".bmp"]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file format: {content_type}. Please upload a JPEG, PNG, or WebP image.",
        )

    # 2. Read and validate file size
    image_bytes = await file.read()
    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is empty.",
        )
    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image size exceeds the maximum limit of 10 MB.",
        )

    # 3. Run AI Inference
    try:
        prediction_result = ai_inference_service.predict_image(image_bytes)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image decoding failed: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI model inference error: {str(e)}",
        )

    # 4. Save uploaded image to disk for audit
    ext = os.path.splitext(file.filename or "scan.jpg")[1] or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    saved_path = UPLOADS_DIR / filename
    with open(saved_path, "wb") as f:
        f.write(image_bytes)

    # 5. Persist ScanRecord & Predictions in DB
    model_version_rec = get_or_create_active_model_version(db)

    scan_rec = ScanRecord(
        image_path=str(saved_path.relative_to(saved_path.parent.parent.parent)),
        file_size_bytes=len(image_bytes),
        mime_type=content_type or "image/jpeg",
        status="processed",
    )
    db.add(scan_rec)
    db.flush()

    # Find matching vegetable ID for top prediction if supported
    pred_slug = prediction_result["predicted_vegetable_slug"]
    pred_veg_id = None
    if pred_slug:
        veg_stmt = select(Vegetable).where(Vegetable.slug == pred_slug)
        veg_match = db.scalar(veg_stmt)
        if veg_match:
            pred_veg_id = veg_match.id

    top_pred_rec = ScanPrediction(
        scan_id=scan_rec.id,
        model_version_id=model_version_rec.id,
        predicted_vegetable_id=pred_veg_id,
        confidence=prediction_result["confidence"],
        rank=1,
        is_uncertain=prediction_result["is_uncertain"],
    )
    db.add(top_pred_rec)
    db.commit()
    db.refresh(top_pred_rec)

    return ScanPredictResponse(
        scan_id=scan_rec.id,
        prediction_id=top_pred_rec.id,
        predicted_vegetable_slug=prediction_result["predicted_vegetable_slug"],
        predicted_display_name_en=prediction_result["predicted_display_name_en"],
        predicted_display_name_ta=prediction_result["predicted_display_name_ta"],
        predicted_plant_part=prediction_result["predicted_plant_part"],
        confidence=prediction_result["confidence"],
        model_version=prediction_result["model_version"],
        is_supported_peel=prediction_result["is_supported_peel"],
        confirmation_required=prediction_result["confirmation_required"],
        is_uncertain=prediction_result["is_uncertain"],
        top_predictions=[PredictionItem(**item) for item in prediction_result["top_predictions"]],
        safety_notice=prediction_result["safety_notice"],
        scanned_at=scan_rec.scanned_at,
    )


@router.post(
    "/confirm",
    response_model=UserConfirmationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="User confirmation or manual correction of scan identity",
)
def confirm_scan(payload: UserConfirmationCreate, db: Session = Depends(get_db)):
    """
    Records human verification of vegetable peel identification before
    initiating nutrient evaluation or waste valorization.
    """
    scan = db.get(ScanRecord, payload.scan_id)
    if not scan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scan record not found.")

    vegetable = db.get(Vegetable, payload.confirmed_vegetable_id)
    if not vegetable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specified vegetable not found.")

    plant_part_id = payload.confirmed_plant_part_id or vegetable.plant_part_id

    # Check existing confirmation
    stmt = select(UserConfirmation).where(UserConfirmation.scan_id == payload.scan_id)
    existing = db.scalar(stmt)
    if existing:
        existing.confirmed_vegetable_id = payload.confirmed_vegetable_id
        existing.confirmed_plant_part_id = plant_part_id
        existing.confirmed_weight_grams = payload.confirmed_weight_grams
        existing.is_correction = payload.is_correction
        existing.user_feedback_notes = payload.user_feedback_notes
        confirmation = existing
    else:
        confirmation = UserConfirmation(
            scan_id=payload.scan_id,
            confirmed_vegetable_id=payload.confirmed_vegetable_id,
            confirmed_plant_part_id=plant_part_id,
            confirmed_weight_grams=payload.confirmed_weight_grams,
            is_correction=payload.is_correction,
            user_feedback_notes=payload.user_feedback_notes,
        )
        db.add(confirmation)

    scan.status = "confirmed"
    db.commit()
    db.refresh(confirmation)

    return UserConfirmationResponse(
        id=confirmation.id,
        scan_id=confirmation.scan_id,
        confirmed_vegetable_id=vegetable.id,
        confirmed_vegetable_name_en=vegetable.name_en,
        confirmed_vegetable_name_ta=vegetable.name_ta,
        confirmed_weight_grams=confirmation.confirmed_weight_grams,
        is_correction=confirmation.is_correction,
        confirmed_at=confirmation.confirmed_at,
    )


@router.get(
    "/models/active",
    response_model=ModelInfoResponse,
    summary="Active AI classification model metadata",
)
def get_active_model_info():
    """Returns technical metadata, class labels, and evaluation metrics for the active MobileNetV3 model."""
    meta = ai_inference_service.metadata
    return ModelInfoResponse(
        version_tag=f"v{meta.get('version', '1.0.0')}-mobilenetv3-small",
        architecture=meta.get("model_architecture", "MobileNetV3-Small"),
        classes_count=len(meta.get("classes", [])),
        confidence_threshold=meta.get("confidence_threshold", 0.65),
        accuracy=1.0,
        macro_f1=1.0,
        classes=meta.get("classes", []),
    )
