import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_user_registration_and_login_flow():
    # 1. Register new user
    register_payload = {
        "email": "researcher@smartpeel.ai",
        "password": "SecurePassword123!",
        "full_name": "Dr. Ananya Raman",
        "preferred_language": "ta",
    }
    reg_res = client.post("/api/v1/auth/register", json=register_payload)
    assert reg_res.status_code == 201
    user_data = reg_res.json()
    assert user_data["email"] == "researcher@smartpeel.ai"
    assert user_data["full_name"] == "Dr. Ananya Raman"
    assert user_data["preferred_language"] == "ta"
    assert "password" not in user_data
    assert "hashed_password" not in user_data

    # 2. Reject duplicate email
    dup_res = client.post("/api/v1/auth/register", json=register_payload)
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"].lower()

    # 3. Successful login returns JWT token
    login_payload = {
        "email": "researcher@smartpeel.ai",
        "password": "SecurePassword123!",
    }
    login_res = client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    token = token_data["access_token"]

    # 4. Access protected /auth/me
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "researcher@smartpeel.ai"

    # 5. Update user profile
    update_res = client.put(
        "/api/v1/auth/me",
        json={"full_name": "Dr. Ananya Raman, PhD", "preferred_language": "en"},
        headers=headers,
    )
    assert update_res.status_code == 200
    assert update_res.json()["full_name"] == "Dr. Ananya Raman, PhD"
    assert update_res.json()["preferred_language"] == "en"

    # 6. Change password
    pwd_res = client.put(
        "/api/v1/auth/me/password",
        json={"old_password": "SecurePassword123!", "new_password": "NewUltraSecretPassword456!"},
        headers=headers,
    )
    assert pwd_res.status_code == 200

    # 7. Old password fails
    old_login = client.post("/api/v1/auth/login", json=login_payload)
    assert old_login.status_code == 401

    # 8. New password succeeds
    new_login = client.post(
        "/api/v1/auth/login",
        json={"email": "researcher@smartpeel.ai", "password": "NewUltraSecretPassword456!"},
    )
    assert new_login.status_code == 200
    new_token = new_login.json()["access_token"]
    new_headers = {"Authorization": f"Bearer {new_token}"}

    # 9. Get user history
    hist_res = client.get("/api/v1/auth/history", headers=new_headers)
    assert hist_res.status_code == 200
    assert isinstance(hist_res.json(), list)

    # 10. Delete account
    del_res = client.delete("/api/v1/auth/me", headers=new_headers)
    assert del_res.status_code == 204

    # 11. Subsequent login fails
    post_del_login = client.post(
        "/api/v1/auth/login",
        json={"email": "researcher@smartpeel.ai", "password": "NewUltraSecretPassword456!"},
    )
    assert post_del_login.status_code == 401


def test_password_reset_workflow():
    # 1. Register a user for reset test
    user_payload = {
        "email": "reset_test@smartpeel.ai",
        "password": "InitialPassword123!",
        "full_name": "Test User Reset",
        "preferred_language": "en",
    }
    client.post("/api/v1/auth/register", json=user_payload)

    # 2. Request reset token
    req_res = client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": "reset_test@smartpeel.ai"},
    )
    assert req_res.status_code == 200
    token = req_res.json().get("reset_token")
    assert token is not None

    # 3. Invalid token fails
    bad_confirm = client.post(
        "/api/v1/auth/password-reset/confirm",
        json={
            "email": "reset_test@smartpeel.ai",
            "reset_token": "INVALID_TOKEN_STRING",
            "new_password": "NewPasswordViaReset123!",
        },
    )
    assert bad_confirm.status_code == 400

    # 4. Valid token succeeds
    good_confirm = client.post(
        "/api/v1/auth/password-reset/confirm",
        json={
            "email": "reset_test@smartpeel.ai",
            "reset_token": token,
            "new_password": "NewPasswordViaReset123!",
        },
    )
    assert good_confirm.status_code == 200

    # 5. Log in with newly reset password
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "reset_test@smartpeel.ai", "password": "NewPasswordViaReset123!"},
    )
    assert login_res.status_code == 200


def test_protected_endpoint_without_token_returns_401():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
