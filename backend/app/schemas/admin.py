from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class AdminOverviewMetrics(BaseModel):
    total_vegetables: int
    total_scans: int
    total_confirmed_scans: int
    total_waste_logs: int
    total_waste_diverted_kg: float
    total_co2_saved_kg: float
    total_users: int
    active_users: int
    superuser_count: int
    total_safety_rules: int
    total_valorization_methods: int
    active_ai_model: Optional[str]
    active_ai_version: Optional[str]
    system_status: str
    db_status: str


class AuditLogEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int]
    user_email: Optional[str] = None
    action: str
    target_table: str
    record_id: Optional[int]
    details: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    timestamp: datetime


class AuditLogCreate(BaseModel):
    action: str = Field(..., min_length=2, max_length=100)
    target_table: str = Field(..., min_length=2, max_length=50)
    record_id: Optional[int] = None
    details: Optional[Dict[str, Any]] = None


class AdminUserListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    role_name: str
    is_active: bool
    is_superuser: bool
    preferred_language: str
    created_at: datetime
    scan_count: int = 0
    waste_log_count: int = 0


class AdminUserStatusUpdate(BaseModel):
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class SystemDiagnostics(BaseModel):
    database: Dict[str, Any]
    ai_model_service: Dict[str, Any]
    storage: Dict[str, Any]
    timestamp: datetime
