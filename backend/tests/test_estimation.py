import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_peel_yield_ratios():
    response = client.get("/api/v1/nutrients/yield-ratios")
    assert response.status_code == 200
    ratios = response.json()
    assert len(ratios) == 50
    slugs = [r["vegetable_slug"] for r in ratios]
    assert "carrot" in slugs
    assert "potato" in slugs
    assert "ridge-gourd" in slugs
    assert "cucumber" in slugs
    assert "onion" in slugs


def test_get_peel_yield_ratio_by_slug():
    response = client.get("/api/v1/nutrients/yield-ratios/potato")
    assert response.status_code == 200
    ratio = response.json()
    assert ratio["vegetable_slug"] == "potato"
    assert ratio["average_peel_percentage"] == 11.5
    assert ratio["min_peel_percentage"] == 8.0
    assert ratio["max_peel_percentage"] == 15.0
    assert ratio["moisture_percentage_fresh"] == 81.0
    assert ratio["dry_matter_percentage"] == 19.0
    assert "chlorogenic acid" in ratio["pulp_comparison_notes_en"]
    assert ratio["pulp_comparison_notes_ta"] is not None


def test_get_nonexistent_peel_yield_ratio():
    response = client.get("/api/v1/nutrients/yield-ratios/nonexistent-slug")
    assert response.status_code == 404


def test_list_daily_reference_intakes():
    response = client.get("/api/v1/nutrients/dri")
    assert response.status_code == 200
    dris = response.json()
    assert len(dris) >= 60
    groups = set(d["population_group"] for d in dris)
    assert "adult_male" in groups
    assert "adult_female" in groups
    assert "pregnant_woman" in groups
    assert "children_7_9y" in groups


def test_filter_daily_reference_intakes():
    response = client.get("/api/v1/nutrients/dri?population_group=adult_male&nutrient_code=vit_c")
    assert response.status_code == 200
    dris = response.json()
    assert len(dris) == 1
    assert dris[0]["nutrient_code"] == "vit_c"
    assert dris[0]["population_group"] == "adult_male"
    assert dris[0]["rda_value"] == 80.0
    assert dris[0]["unit"] == "mg"


def test_estimate_nutrients_direct_peel():
    payload = {
        "vegetable_slug": "carrot",
        "input_weight_grams": 100.0,
        "input_weight_type": "peel",
        "preparation_method": "fresh_raw",
        "population_group": "adult_male",
        "servings": 1,
    }
    response = client.post("/api/v1/nutrients/estimate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["vegetable_slug"] == "carrot"
    assert data["calculated_peel_weight_grams"] == 100.0
    assert data["preparation_method"] == "fresh_raw"
    assert data["population_group"] == "adult_male"
    assert data["environmental_impact"]["wet_waste_diverted_kg"] == 0.1
    assert data["environmental_impact"]["ghg_emissions_avoided_kg_co2e"] == 0.052

    # Verify nutrients calculated
    nutrients = {n["nutrient_code"]: n for n in data["nutrients"]}
    assert "vit_a" in nutrients
    assert "vit_c" in nutrients

    # Check retention factor for raw is 1.0
    assert nutrients["vit_c"]["retention_factor"] == 1.0
    assert nutrients["vit_c"]["estimated_amount"] > 0
    assert nutrients["vit_c"]["percentage_rda"] is not None


def test_estimate_nutrients_whole_vegetable():
    # 500g whole potato with 11.5% peel yield ratio -> 57.5g peel
    payload = {
        "vegetable_slug": "potato",
        "input_weight_grams": 500.0,
        "input_weight_type": "whole_vegetable",
        "preparation_method": "fresh_raw",
        "population_group": "adult_female",
        "servings": 2,
    }
    response = client.post("/api/v1/nutrients/estimate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["vegetable_slug"] == "potato"
    assert data["input_weight_grams"] == 500.0
    assert data["input_weight_type"] == "whole_vegetable"
    assert abs(data["calculated_peel_weight_grams"] - 57.5) < 0.1
    assert data["peel_weight_range_grams"]["min"] == 40.0  # 500 * 8%
    assert data["peel_weight_range_grams"]["max"] == 75.0  # 500 * 15%
    assert data["servings"] == 2

    # Per serving should be half of total estimated amount
    for n in data["nutrients"]:
        assert abs(n["estimated_amount_per_serving"] - (n["estimated_amount"] / 2.0)) < 0.01


def test_estimate_nutrients_cooking_retention_factors():
    # Test sautéed cooking method thermal degradation
    payload_raw = {
        "vegetable_slug": "carrot",
        "input_weight_grams": 100.0,
        "input_weight_type": "peel",
        "preparation_method": "fresh_raw",
        "population_group": "adult_male",
    }
    res_raw = client.post("/api/v1/nutrients/estimate", json=payload_raw).json()

    payload_sauteed = {
        "vegetable_slug": "carrot",
        "input_weight_grams": 100.0,
        "input_weight_type": "peel",
        "preparation_method": "sauteed",
        "population_group": "adult_male",
    }
    res_sauteed = client.post("/api/v1/nutrients/estimate", json=payload_sauteed).json()

    raw_vit_c = next(n for n in res_raw["nutrients"] if n["nutrient_code"] == "vit_c")
    sauteed_vit_c = next(n for n in res_sauteed["nutrients"] if n["nutrient_code"] == "vit_c")

    assert sauteed_vit_c["retention_factor"] == 0.80
    assert abs(sauteed_vit_c["estimated_amount"] - (raw_vit_c["estimated_amount"] * 0.80)) < 0.05


def test_save_and_retrieve_nutrient_report():
    # 1. Estimate
    est_payload = {
        "vegetable_slug": "ridge-gourd",
        "input_weight_grams": 150.0,
        "input_weight_type": "peel",
        "preparation_method": "sauteed",
        "population_group": "adult_male",
    }
    est_res = client.post("/api/v1/nutrients/estimate", json=est_payload)
    assert est_res.status_code == 200
    est_data = est_res.json()

    # 2. Save report
    save_payload = {
        "vegetable_id": est_data["vegetable_id"],
        "total_weight_grams": est_data["calculated_peel_weight_grams"],
        "calculations": est_data,
        "safety_notes": {"status": "safe_edible", "hazards": []},
        "user_feedback_notes": "Tested in kitchen preparation.",
    }
    save_res = client.post("/api/v1/nutrients/reports/save", json=save_payload)
    assert save_res.status_code == 201
    report = save_res.json()
    assert "report_uuid" in report
    assert report["report_uuid"].startswith("RPT-")
    assert report["total_weight_grams"] == 150.0

    # 3. Retrieve report
    get_res = client.get(f"/api/v1/nutrients/reports/{report['report_uuid']}")
    assert get_res.status_code == 200
    retrieved = get_res.json()
    assert retrieved["report_uuid"] == report["report_uuid"]
    assert retrieved["calculations"]["vegetable_slug"] == "ridge-gourd"


def test_estimate_invalid_vegetable():
    payload = {
        "vegetable_slug": "nonexistent-item-xyz",
        "input_weight_grams": 100.0,
    }
    response = client.post("/api/v1/nutrients/estimate", json=payload)
    assert response.status_code == 404


def test_estimate_invalid_weight():
    payload = {
        "vegetable_slug": "carrot",
        "input_weight_grams": -50.0,
    }
    response = client.post("/api/v1/nutrients/estimate", json=payload)
    assert response.status_code == 422


def test_estimate_pregnant_woman_demographic():
    payload = {
        "vegetable_slug": "beetroot",
        "input_weight_grams": 100.0,
        "input_weight_type": "peel",
        "preparation_method": "sauteed",
        "population_group": "pregnant_woman",
    }
    response = client.post("/api/v1/nutrients/estimate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["population_group"] == "pregnant_woman"
    assert "Pregnant" in data["population_group_label_en"]
    assert "கர்ப்பிணி" in data["population_group_label_ta"]


def test_estimate_children_demographic():
    payload = {
        "vegetable_slug": "carrot",
        "input_weight_grams": 80.0,
        "input_weight_type": "peel",
        "preparation_method": "fresh_raw",
        "population_group": "children_7_9y",
    }
    response = client.post("/api/v1/nutrients/estimate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["population_group"] == "children_7_9y"


def test_estimate_boiled_drained_and_dried_powder():
    # Boiled drained
    payload_boiled = {
        "vegetable_slug": "potato",
        "input_weight_grams": 100.0,
        "preparation_method": "boiled_drained",
    }
    res_boiled = client.post("/api/v1/nutrients/estimate", json=payload_boiled)
    assert res_boiled.status_code == 200
    data_boiled = res_boiled.json()
    assert data_boiled["preparation_method"] == "boiled_drained"

    # Dried powder
    payload_powder = {
        "vegetable_slug": "onion",
        "input_weight_grams": 50.0,
        "preparation_method": "dried_powder",
    }
    res_powder = client.post("/api/v1/nutrients/estimate", json=payload_powder)
    assert res_powder.status_code == 200
    data_powder = res_powder.json()
    assert data_powder["preparation_method"] == "dried_powder"


def test_get_nonexistent_report():
    response = client.get("/api/v1/nutrients/reports/RPT-NONEXISTENT999")
    assert response.status_code == 404


def test_estimate_by_vegetable_id():
    payload = {
        "vegetable_id": 1,  # carrot
        "input_weight_grams": 120.0,
        "input_weight_type": "peel",
    }
    response = client.post("/api/v1/nutrients/estimate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["vegetable_id"] == 1
    assert data["vegetable_slug"] == "carrot"

