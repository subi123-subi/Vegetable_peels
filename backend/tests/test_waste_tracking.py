import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_diverted_waste_log():
    payload = {
        "vegetable_slug": "carrot",
        "plant_part_code": "peel",
        "weight_grams": 350.0,
        "reuse_method_code": "aerobic_composting",
        "is_diverted": True,
        "notes": "Home kitchen compost bin",
    }
    response = client.post("/api/v1/waste-tracking/log", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["vegetable_slug"] == "carrot"
    assert data["weight_grams"] == 350.0
    assert data["weight_kg"] == 0.35
    assert data["is_diverted"] is True
    assert data["diversion_category"] == "composting"
    assert data["reuse_method_code"] == "aerobic_composting"


def test_create_non_diverted_waste_log():
    payload = {
        "vegetable_slug": "potato",
        "plant_part_code": "peel",
        "weight_grams": 500.0,
        "is_diverted": False,
        "notes": "Discarded to mixed household garbage",
    }
    response = client.post("/api/v1/waste-tracking/log", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["is_diverted"] is False
    assert data["diversion_category"] == "landfill_disposal"
    assert data["weight_kg"] == 0.5


def test_create_waste_log_invalid_vegetable_fails():
    payload = {
        "vegetable_slug": "unknown_vegetable_xyz",
        "weight_grams": 100.0,
    }
    response = client.post("/api/v1/waste-tracking/log", json=payload)
    assert response.status_code == 404


def test_list_waste_logs():
    response = client.get("/api/v1/waste-tracking/logs")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_list_waste_logs_filtered():
    # Filter by is_diverted=True
    response = client.get("/api/v1/waste-tracking/logs?is_diverted=true")
    assert response.status_code == 200
    for log in response.json():
        assert log["is_diverted"] is True

    # Filter by is_diverted=False
    response_false = client.get("/api/v1/waste-tracking/logs?is_diverted=false")
    assert response_false.status_code == 200
    for log in response_false.json():
        assert log["is_diverted"] is False


def test_get_waste_summary_analytics():
    response = client.get("/api/v1/waste-tracking/summary")
    assert response.status_code == 200
    data = response.json()

    assert data["total_recorded_waste_kg"] > 0
    assert data["total_diverted_waste_kg"] >= 0
    assert 0.0 <= data["diversion_rate_percentage"] <= 100.0
    assert data["total_logs_count"] >= 2
    assert len(data["by_category"]) >= 1
    assert len(data["daily_totals"]) >= 1


def test_delete_waste_log():
    # 1. Create a log
    create_res = client.post(
        "/api/v1/waste-tracking/log",
        json={
            "vegetable_slug": "beetroot",
            "weight_grams": 200.0,
            "is_diverted": True,
        },
    )
    log_id = create_res.json()["id"]

    # 2. Delete it
    del_res = client.delete(f"/api/v1/waste-tracking/logs/{log_id}")
    assert del_res.status_code == 204

    # 3. Confirm deletion
    del_res_again = client.delete(f"/api/v1/waste-tracking/logs/{log_id}")
    assert del_res_again.status_code == 404
