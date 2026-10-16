import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import create_access_token
from app.db.session import SessionLocal
from app.models.user import User, UserRole, AdminAuditLog


@pytest.fixture(scope="module")
def admin_client():
    return TestClient(app)


@pytest.fixture(scope="module")
def superuser_token():
    db = SessionLocal()
    try:
        # Find or create a superuser
        user = db.query(User).filter(User.is_superuser == True).first()
        if not user:
            role = db.query(UserRole).filter(UserRole.name == "admin").first()
            if not role:
                role = UserRole(name="admin", description="Admin role")
                db.add(role)
                db.commit()
                db.refresh(role)
            user = User(
                email="superadmin_test@smartpeel.ai",
                hashed_password="hashed_pw_test",
                full_name="Super Admin",
                role_id=role.id,
                is_active=True,
                is_superuser=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        token = create_access_token(subject=user.id)
        return token, user.id
    finally:
        db.close()


@pytest.fixture(scope="module")
def normal_user_token():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.is_superuser == False).first()
        if not user:
            role = db.query(UserRole).filter(UserRole.name == "user").first()
            if not role:
                role = UserRole(name="user", description="Normal user")
                db.add(role)
                db.commit()
                db.refresh(role)
            user = User(
                email="regular_user_test@smartpeel.ai",
                hashed_password="hashed_pw_test",
                full_name="Regular User",
                role_id=role.id,
                is_active=True,
                is_superuser=False,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        token = create_access_token(subject=user.id)
        return token, user.id
    finally:
        db.close()


def test_admin_overview_requires_auth(admin_client):
    """Accessing admin overview without authentication must yield 401."""
    resp = admin_client.get("/api/v1/admin/overview")
    assert resp.status_code == 401


def test_admin_overview_forbidden_for_regular_user(admin_client, normal_user_token):
    """Accessing admin overview as a non-superuser must yield 403."""
    token, _ = normal_user_token
    resp = admin_client.get(
        "/api/v1/admin/overview",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403


def test_admin_overview_success(admin_client, superuser_token):
    """Superuser can successfully query system overview metrics."""
    token, _ = superuser_token
    resp = admin_client.get(
        "/api/v1/admin/overview",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "total_vegetables" in data
    assert data["total_vegetables"] >= 50
    assert "total_users" in data
    assert "total_safety_rules" in data
    assert "active_ai_model" in data
    assert data["system_status"] == "HEALTHY"
    assert data["db_status"] == "CONNECTED"


def test_admin_audit_logs_workflow(admin_client, superuser_token):
    """Superuser can record and retrieve audit log entries."""
    token, admin_id = superuser_token

    # 1. Post a new audit log
    create_resp = admin_client.post(
        "/api/v1/admin/audit-logs",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "action": "CONFIG_UPDATE_TEST",
            "target_table": "system_settings",
            "record_id": 999,
            "details": {"key": "test_param", "value": 42},
        },
    )
    assert create_resp.status_code == 201
    log_data = create_resp.json()
    assert log_data["action"] == "CONFIG_UPDATE_TEST"
    assert log_data["user_id"] == admin_id

    # 2. Query audit logs
    list_resp = admin_client.get(
        "/api/v1/admin/audit-logs?action=CONFIG_UPDATE_TEST",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_resp.status_code == 200
    entries = list_resp.json()
    assert len(entries) >= 1
    assert any(e["action"] == "CONFIG_UPDATE_TEST" for e in entries)


def test_admin_users_list_and_status_update(admin_client, superuser_token, normal_user_token):
    """Superuser can view users list and update user status."""
    token, admin_id = superuser_token
    _, normal_id = normal_user_token

    # List users
    users_resp = admin_client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert users_resp.status_code == 200
    users = users_resp.json()
    assert len(users) >= 2

    # Update normal user status
    patch_resp = admin_client.patch(
        f"/api/v1/admin/users/{normal_id}/status",
        headers={"Authorization": f"Bearer {token}"},
        json={"is_active": True},
    )
    assert patch_resp.status_code == 200
    assert patch_resp.json()["is_active"] is True

    # Prevent admin from deactivating self
    self_patch = admin_client.patch(
        f"/api/v1/admin/users/{admin_id}/status",
        headers={"Authorization": f"Bearer {token}"},
        json={"is_active": False},
    )
    assert self_patch.status_code == 400


def test_admin_diagnostics(admin_client, superuser_token):
    """Superuser can fetch deep system diagnostics."""
    token, _ = superuser_token
    diag_resp = admin_client.get(
        "/api/v1/admin/diagnostics",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert diag_resp.status_code == 200
    data = diag_resp.json()
    assert "database" in data
    assert data["database"]["connected"] is True
    assert "ai_model_service" in data
    assert "storage" in data


def test_admin_refresh_model_cache(admin_client, superuser_token):
    """Superuser can trigger AI model cache reloading."""
    token, _ = superuser_token
    refresh_resp = admin_client.post(
        "/api/v1/admin/ai-models/refresh-cache",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert refresh_resp.status_code == 200
    assert refresh_resp.json()["status"] == "success"
