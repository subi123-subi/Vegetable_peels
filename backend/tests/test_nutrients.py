import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_all_nutrients():
    response = client.get("/api/v1/nutrients/")
    assert response.status_code == 200
    nutrients = response.json()
    assert len(nutrients) >= 29
    codes = [n["code"] for n in nutrients]
    assert "vit_a" in codes
    assert "vit_c" in codes
    assert "calcium" in codes
    assert "potassium" in codes
    assert "dietary_fibre" in codes


def test_filter_nutrients_by_vitamin():
    response = client.get("/api/v1/nutrients/?category=vitamin")
    assert response.status_code == 200
    vitamins = response.json()
    assert len(vitamins) >= 12
    for v in vitamins:
        assert v["category"] == "vitamin"


def test_filter_nutrients_by_mineral():
    response = client.get("/api/v1/nutrients/?category=mineral")
    assert response.status_code == 200
    minerals = response.json()
    assert len(minerals) >= 10
    for m in minerals:
        assert m["category"] == "mineral"


def test_get_nutrient_categories():
    response = client.get("/api/v1/nutrients/categories")
    assert response.status_code == 200
    cats = response.json()
    assert len(cats) >= 3
    cat_names = [c["category"] for c in cats]
    assert "vitamin" in cat_names
    assert "mineral" in cat_names


def test_get_scientific_sources():
    response = client.get("/api/v1/nutrients/sources")
    assert response.status_code == 200
    sources = response.json()
    assert len(sources) >= 3
    titles = [s["title"] for s in sources]
    assert any("IFCT" in t for t in titles)
    assert any("USDA" in t for t in titles)


def test_get_vegetable_nutrient_profile_carrot():
    response = client.get("/api/v1/nutrients/profiles/carrot")
    assert response.status_code == 200
    profile = response.json()
    assert profile["vegetable_slug"] == "carrot"
    assert profile["fresh_or_dry_basis"] == "fresh_weight"
    assert profile["data_quality_status"] == "validated_peel_measurement"
    assert len(profile["measurements"]) >= 5
    meas_codes = [m["nutrient_code"] for m in profile["measurements"]]
    assert "vit_a" in meas_codes
    assert "vit_c" in meas_codes


def test_get_vegetable_nutrient_profile_onion_dry_basis():
    response = client.get("/api/v1/nutrients/profiles/onion")
    assert response.status_code == 200
    profile = response.json()
    assert profile["vegetable_slug"] == "onion"
    assert profile["fresh_or_dry_basis"] == "dry_weight"
    meas_codes = [m["nutrient_code"] for m in profile["measurements"]]
    assert "quercetin" in meas_codes


def test_get_nutrient_detail_with_top_sources():
    response = client.get("/api/v1/nutrients/vit_c")
    assert response.status_code == 200
    nutrient = response.json()
    assert nutrient["code"] == "vit_c"
    assert len(nutrient["top_peel_sources"]) >= 2
    # Verify sources are sorted by concentration descending
    concs = [s["concentration_per_100g"] for s in nutrient["top_peel_sources"]]
    assert concs == sorted(concs, reverse=True)


def test_get_nonexistent_profile():
    response = client.get("/api/v1/nutrients/profiles/nonexistent-item")
    assert response.status_code == 404


import uuid


def test_create_nutrient_and_measurement():
    unique_code = f"test_lutein_{uuid.uuid4().hex[:8]}"
    # 1. Create unique nutrient
    payload = {
        "code": unique_code,
        "name_en": "Test Lutein",
        "name_ta": "சோதனை லுடீன்",
        "category": "other",
        "standard_unit": "mcg",
        "biological_role_en": "Macular carotenoid for eye health.",
        "biological_role_ta": "கண் பார்வைக்கு உதவும் கரோட்டினாய்டு.",
    }
    create_res = client.post("/api/v1/nutrients/", json=payload)
    assert create_res.status_code == 201
    created_id = create_res.json()["id"]

    # 2. Reject duplicate code
    dup_res = client.post("/api/v1/nutrients/", json=payload)
    assert dup_res.status_code == 400

    # 3. Add verified measurement to Carrot profile (profile_id = 1)
    meas_payload = {
        "profile_id": 1,
        "nutrient_id": created_id,
        "concentration_per_100g": 145.0,
        "unit": "mcg",
        "measurement_method": "HPLC-DAD",
        "min_value": 130.0,
        "max_value": 160.0,
        "confidence_interval": "±10.3%",
    }
    meas_res = client.post("/api/v1/nutrients/measurements", json=meas_payload)
    assert meas_res.status_code == 201
    meas_id = meas_res.json()["measurement_id"]

    # Clean up created test data so it doesn't pollute the database
    from app.db.session import SessionLocal
    from app.models.nutrient import Nutrient, NutrientMeasurement

    db = SessionLocal()
    try:
        db.query(NutrientMeasurement).filter(NutrientMeasurement.id == meas_id).delete()
        db.query(Nutrient).filter(Nutrient.id == created_id).delete()
        db.commit()
    finally:
        db.close()

