import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_all_vegetables():
    response = client.get("/api/v1/vegetables/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 50
    assert len(data["items"]) >= 50


def test_filter_ai_supported_vegetables():
    response = client.get("/api/v1/vegetables/?is_ai_supported=true")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 5
    ai_slugs = {item["slug"] for item in data["items"]}
    assert {"carrot", "potato", "beetroot", "cucumber", "pumpkin"}.issubset(ai_slugs)


def test_filter_by_root_category():
    response = client.get("/api/v1/vegetables/?category=Root")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 12


def test_filter_by_gourd_category():
    response = client.get("/api/v1/vegetables/?category=Gourd")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 15


def test_search_vegetable_english():
    response = client.get("/api/v1/vegetables/?search=Carrot")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert data["items"][0]["slug"] == "carrot"


def test_search_vegetable_tamil():
    response = client.get("/api/v1/vegetables/?search=கேரட்")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert data["items"][0]["name_ta"] == "கேரட்"


def test_get_vegetable_detail_slug():
    response = client.get("/api/v1/vegetables/potato")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == "potato"
    assert data["name_en"] == "Potato"
    assert data["name_ta"] == "உருளைக்கிழங்கு"
    assert data["scientific_name"] == "Solanum tuberosum"
    assert data["is_ai_supported"] is True
    assert data["ai_class_name"] == "potato_peel"
    assert "Solanine" in data["known_hazards_en"]
    assert data["plant_part"]["code"] == "peel"


def test_get_vegetable_not_found():
    response = client.get("/api/v1/vegetables/non-existent-vegetable-xyz")
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"]
