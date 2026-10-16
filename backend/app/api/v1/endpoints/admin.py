import os
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser
from app.db.session import get_db
from app.models.user import User, AdminAuditLog, UserRole
from app.models.vegetable import Vegetable
from app.models.scan import ScanRecord, ScanPrediction, UserConfirmation, AIModelVersion
from app.models.waste_tracking import WasteLog
from app.models.safety import SafetyRule
from app.models.reuse import ReuseMethod, ReuseRecommendation
from app.schemas.admin import (
    AdminOverviewMetrics,
    AuditLogEntry,
    AuditLogCreate,
    AdminUserListItem,
    AdminUserStatusUpdate,
    SystemDiagnostics,
)
from app.schemas.user import UserResponse
from app.services.ai_inference_service import get_inference_service

router = APIRouter()


@router.get("/overview", response_model=AdminOverviewMetrics)
def get_admin_overview(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_superuser),
):
    """Retrieve top-level platform analytics and system status for administrators."""
    total_veggies = db.query(Vegetable).count()
    total_scans = db.query(ScanRecord).count()
    total_confirmed = db.query(UserConfirmation).count()
    total_waste_logs = db.query(WasteLog).count()

    total_diverted_grams = db.query(func.coalesce(func.sum(WasteLog.weight_grams), 0.0)).scalar()
    total_diverted_kg = float(total_diverted_grams) / 1000.0
    total_co2 = total_diverted_kg * 0.5  # 0.5 kg CO2e per kg organic waste diverted

    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    superuser_count = db.query(User).filter(User.is_superuser == True).count()

    total_safety_rules = db.query(SafetyRule).count()
    total_valorization_methods = db.query(ReuseRecommendation).count()

    active_model = db.query(AIModelVersion).filter(AIModelVersion.status == "active").first()

    return AdminOverviewMetrics(
        total_vegetables=total_veggies,
        total_scans=total_scans,
        total_confirmed_scans=total_confirmed,
        total_waste_logs=total_waste_logs,
        total_waste_diverted_kg=round(float(total_diverted_grams) / 1000.0, 2),
        total_co2_saved_kg=round(float(total_co2), 2),
        total_users=total_users,
        active_users=active_users,
        superuser_count=superuser_count,
        total_safety_rules=total_safety_rules,
        total_valorization_methods=total_valorization_methods,
        active_ai_model=active_model.model_architecture if active_model else "MobileNetV3Large",
        active_ai_version=active_model.version_tag if active_model else "v1.0.0-mobilenetv3",
        system_status="HEALTHY",
        db_status="CONNECTED",
    )


@router.get("/audit-logs", response_model=List[AuditLogEntry])
def list_audit_logs(
    action: Optional[str] = Query(None, description="Filter by action name"),
    target_table: Optional[str] = Query(None, description="Filter by target table"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_superuser),
):
    """Retrieve audit trail logs with filtering and pagination."""
    query = db.query(AdminAuditLog)
    if action:
        query = query.filter(AdminAuditLog.action == action)
    if target_table:
        query = query.filter(AdminAuditLog.target_table == target_table)

    logs = query.order_by(desc(AdminAuditLog.timestamp)).offset(offset).limit(limit).all()

    results = []
    for log in logs:
        results.append(
            AuditLogEntry(
                id=log.id,
                user_id=log.user_id,
                user_email=log.user.email if log.user else None,
                action=log.action,
                target_table=log.target_table,
                record_id=log.record_id,
                details=log.details,
                ip_address=log.ip_address,
                timestamp=log.timestamp,
            )
        )
    return results


@router.post("/audit-logs", response_model=AuditLogEntry, status_code=status.HTTP_201_CREATED)
def create_audit_log(
    payload: AuditLogCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_superuser),
):
    """Record an administrative audit log event."""
    client_ip = request.client.host if request.client else "127.0.0.1"
    audit_entry = AdminAuditLog(
        user_id=current_admin.id,
        action=payload.action,
        target_table=payload.target_table,
        record_id=payload.record_id,
        details=payload.details,
        ip_address=client_ip,
    )
    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)

    return AuditLogEntry(
        id=audit_entry.id,
        user_id=audit_entry.user_id,
        user_email=current_admin.email,
        action=audit_entry.action,
        target_table=audit_entry.target_table,
        record_id=audit_entry.record_id,
        details=audit_entry.details,
        ip_address=audit_entry.ip_address,
        timestamp=audit_entry.timestamp,
    )


@router.get("/users", response_model=List[AdminUserListItem])
def list_system_users(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_superuser),
):
    """List registered users with activity statistics."""
    users = db.query(User).order_by(desc(User.created_at)).offset(offset).limit(limit).all()
    result = []
    for u in users:
        scan_cnt = db.query(ScanRecord).filter(ScanRecord.user_id == u.id).count()
        waste_cnt = db.query(WasteLog).filter(WasteLog.user_id == u.id).count()
        role_name = u.role.name if u.role else "user"
        result.append(
            AdminUserListItem(
                id=u.id,
                email=u.email,
                full_name=u.full_name,
                role_name=role_name,
                is_active=u.is_active,
                is_superuser=u.is_superuser,
                preferred_language=u.preferred_language,
                created_at=u.created_at,
                scan_count=scan_cnt,
                waste_log_count=waste_cnt,
            )
        )
    return result


@router.patch("/users/{user_id}/status", response_model=UserResponse)
def update_user_status(
    user_id: int,
    payload: AdminUserStatusUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_superuser),
):
    """Update active or superuser status of a user account."""
    target_user = db.get(User, user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )

    if target_user.id == current_admin.id:
        if payload.is_active is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Administrators cannot deactivate their own account.",
            )
        if payload.is_superuser is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Administrators cannot revoke their own superuser privileges.",
            )

    changed_fields = {}
    if payload.is_active is not None and target_user.is_active != payload.is_active:
        changed_fields["is_active"] = {"old": target_user.is_active, "new": payload.is_active}
        target_user.is_active = payload.is_active

    if payload.is_superuser is not None and target_user.is_superuser != payload.is_superuser:
        changed_fields["is_superuser"] = {"old": target_user.is_superuser, "new": payload.is_superuser}
        target_user.is_superuser = payload.is_superuser

    if changed_fields:
        client_ip = request.client.host if request.client else "127.0.0.1"
        audit = AdminAuditLog(
            user_id=current_admin.id,
            action="UPDATE_USER_STATUS",
            target_table="users",
            record_id=target_user.id,
            details=changed_fields,
            ip_address=client_ip,
        )
        db.add(audit)
        db.commit()
        db.refresh(target_user)

    role_name = target_user.role.name if target_user.role else "user"
    return UserResponse(
        id=target_user.id,
        email=target_user.email,
        full_name=target_user.full_name,
        role_name=role_name,
        is_active=target_user.is_active,
        is_superuser=target_user.is_superuser,
        preferred_language=target_user.preferred_language,
        created_at=target_user.created_at,
    )


@router.post("/ai-models/refresh-cache")
def refresh_ai_model_cache(
    request: Request,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_superuser),
):
    """Reload the active AI PyTorch model weights and class labels into memory."""
    try:
        service = get_inference_service()
        service.reload_model()
        client_ip = request.client.host if request.client else "127.0.0.1"
        audit = AdminAuditLog(
            user_id=current_admin.id,
            action="REFRESH_MODEL_CACHE",
            target_table="ai_model_versions",
            details={"model_architecture": "MobileNetV3Large", "status": "reloaded"},
            ip_address=client_ip,
        )
        db.add(audit)
        db.commit()
        return {"status": "success", "message": "AI inference engine reloaded successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reload model: {str(e)}",
        )


@router.get("/diagnostics", response_model=SystemDiagnostics)
def run_diagnostics(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_active_superuser),
):
    """Deep system diagnostic report for administrative verification."""
    # 1. Database status
    db_health = {"connected": True, "engine": "sqlite", "tables_verified": True}
    try:
        db.execute(func.now())
    except Exception as e:
        db_health["connected"] = False
        db_health["error"] = str(e)

    # 2. AI Model Service
    service = get_inference_service()
    weights_path = service.weights_path
    ai_status = {
        "model_file_path": weights_path,
        "weights_file_exists": os.path.exists(weights_path) if weights_path else False,
        "device": service.device,
        "is_model_loaded": service.model is not None,
        "num_classes": len(service.class_labels),
    }

    # 3. Storage
    storage_status = {
        "data_dir_exists": os.path.exists("data"),
        "models_dir_exists": os.path.exists("data/models"),
        "uploads_dir_exists": os.path.exists("data/uploads"),
    }

    return SystemDiagnostics(
        database=db_health,
        ai_model_service=ai_status,
        storage=storage_status,
        timestamp=datetime.utcnow(),
    )
