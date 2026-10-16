import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_safety_rules():
    response = client.get("/api/v1/safety/rules")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 4
    codes = [r["code"] for r in data]
    assert "SR_POTATO_SOLANINE" in codes
    assert "SR_CASSAVA_CYANIDE" in codes


def test_list_safety_rules_filtered_by_severity():
    response = client.get("/api/v1/safety/rules?severity=critical")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    for rule in data:
        assert rule["severity"] == "critical"


def test_get_single_safety_rule():
    response = client.get("/api/v1/safety/rules/SR_POTATO_SOLANINE")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SR_POTATO_SOLANINE"
    assert data["hazard_type"] == "glycoalkaloid"
    assert data["severity"] == "critical"
    assert "solanine" in data["rule_description_en"].lower()
    assert data["scientific_reference"] is not None


def test_evaluate_clean_carrot_peel():
    payload = {
        "vegetable_slug": "carrot",
        "conditions": {
            "is_green_or_sprouted": False,
            "is_bitter_tasting": False,
            "has_visible_mould": False,
            "is_unwashed": False,
        },
        "scan_confidence": 0.95,
    }
    response = client.post("/api/v1/safety/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["vegetable_slug"] == "carrot"
    assert data["edible_recommendation_allowed"] is True
    assert data["is_hazardous"] is False
    assert data["overall_safety_status"] == "safe_edible"
    assert len(data["conservative_alternatives"]) >= 3


def test_evaluate_green_potato_peel_triggers_critical_solanine():
    payload = {
        "vegetable_slug": "potato",
        "conditions": {
            "is_green_or_sprouted": True,
            "is_bitter_tasting": False,
            "has_visible_mould": False,
            "is_unwashed": False,
        },
        "scan_confidence": 0.98,
    }
    response = client.post("/api/v1/safety/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["vegetable_slug"] == "potato"
    assert data["edible_recommendation_allowed"] is False
    assert data["is_hazardous"] is True
    assert data["overall_safety_status"] == "critical_hazard_discard"

    hazard_codes = [h["code"] for h in data["active_hazards"]]
    assert "SR_CRITICAL_POTATO_SOLANINE" in hazard_codes


def test_evaluate_bitter_gourd_triggers_cucurbitacin_toxicity():
    payload = {
        "vegetable_slug": "cucumber",
        "conditions": {
            "is_green_or_sprouted": False,
            "is_bitter_tasting": True,
            "has_visible_mould": False,
            "is_unwashed": False,
        },
        "scan_confidence": 0.92,
    }
    response = client.post("/api/v1/safety/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["edible_recommendation_allowed"] is False
    assert data["is_hazardous"] is True
    hazard_codes = [h["code"] for h in data["active_hazards"]]
    assert "SR_CRITICAL_CUCURBITACIN_TOXICITY" in hazard_codes


def test_evaluate_visible_mould_escalates_to_mycotoxin_hazard():
    payload = {
        "vegetable_slug": "pumpkin",
        "conditions": {
            "is_green_or_sprouted": False,
            "is_bitter_tasting": False,
            "has_visible_mould": True,
            "is_unwashed": False,
        },
        "scan_confidence": 0.99,
    }
    response = client.post("/api/v1/safety/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["edible_recommendation_allowed"] is False
    assert data["is_hazardous"] is True
    assert data["overall_safety_status"] == "critical_hazard_discard"
    hazard_codes = [h["code"] for h in data["active_hazards"]]
    assert "SR_CRITICAL_MYCOTOXIN" in hazard_codes


def test_evaluate_low_confidence_prevents_edible_use():
    payload = {
        "vegetable_slug": "carrot",
        "conditions": {
            "is_green_or_sprouted": False,
            "is_bitter_tasting": False,
            "has_visible_mould": False,
            "is_unwashed": False,
        },
        "scan_confidence": 0.52,  # Low confidence (< 0.65)
    }
    response = client.post("/api/v1/safety/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["edible_recommendation_allowed"] is False
    hazard_codes = [h["code"] for h in data["active_hazards"]]
    assert "SR_UNCERTAIN_AI_PREDICTION" in hazard_codes


def test_evaluate_unwashed_triggers_pesticide_cleaning_protocol():
    payload = {
        "vegetable_slug": "carrot",
        "conditions": {
            "is_green_or_sprouted": False,
            "is_bitter_tasting": False,
            "has_visible_mould": False,
            "is_unwashed": True,
        },
        "scan_confidence": 0.95,
    }
    response = client.post("/api/v1/safety/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    hazard_codes = [h["code"] for h in data["active_hazards"]]
    assert "SR_SURFACE_PESTICIDE_RESIDUE" in hazard_codes


def test_evaluate_non_existent_vegetable_returns_404():
    payload = {
        "vegetable_slug": "non_existent_species",
    }
    response = client.post("/api/v1/safety/evaluate", json=payload)
    assert response.status_code == 404
