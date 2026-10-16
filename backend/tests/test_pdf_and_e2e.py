import io
from PIL import Image
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.pdf_report_service import generate_nutrient_pdf


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def create_test_image(color=(220, 100, 30), size=(224, 224)) -> bytes:
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_pdf_generation_direct():
    """Unit test for ReportLab PDF generator service."""
    dummy_data = {
        "vegetable_name_en": "Carrot",
        "vegetable_name_ta": "கேரட்",
        "input_weight_grams": 250.0,
        "calculated_peel_weight_grams": 27.5,
        "peel_yield_percentage": 11.0,
        "dry_matter_weight_grams": 3.3,
        "moisture_weight_grams": 24.2,
        "preparation_method_label_en": "Fresh / Raw Preparation",
        "population_group_label_en": "Adult Female (19-59 yrs)",
        "nutrients": [
            {
                "nutrient_name_en": "Beta-Carotene",
                "category": "vitamin",
                "concentration_per_100g_raw": 8285.0,
                "unit": "mcg",
                "retention_factor": 1.0,
                "estimated_amount": 2278.38,
                "percentage_rda": 47.5,
                "biological_role_en": "Precursor of Vitamin A, visual acuity and immune defense",
            },
            {
                "nutrient_name_en": "Dietary Fibre",
                "category": "proximate",
                "concentration_per_100g_raw": 2.8,
                "unit": "g",
                "retention_factor": 1.0,
                "estimated_amount": 0.77,
                "percentage_rda": 2.6,
                "biological_role_en": "Gastrointestinal motility and glycemic control",
            },
        ],
        "environmental_impact": {
            "wet_waste_diverted_kg": 0.0275,
            "ghg_emissions_avoided_kg_co2e": 0.0143,
            "compost_potential_kg": 0.0069,
        },
        "safety_notes": {"status": "cleared", "hazards": []},
    }

    pdf_bytes = generate_nutrient_pdf(dummy_data, report_uuid="RPT-TEST-001")
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF-")


def test_preview_estimation_pdf_endpoint(client):
    """Test POST /api/v1/nutrients/reports/preview-pdf generates valid PDF stream."""
    payload = {
        "vegetable_slug": "carrot",
        "input_weight_grams": 300.0,
        "input_weight_type": "whole",
        "preparation_method": "fresh_raw",
        "population_group": "adult_male",
        "servings": 1,
    }
    resp = client.post("/api/v1/nutrients/reports/preview-pdf", json=payload)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content.startswith(b"%PDF-")
    assert len(resp.content) > 1000


def test_complete_e2e_smart_peel_system_lifecycle(client):
    """
    Comprehensive End-to-End System Test:
    1. Scan image
    2. Confirm vegetable
    3. Run nutrient calculation
    4. Safety evaluation
    5. Waste valorization recommendations
    6. Log diverted waste
    7. Save archive report
    8. Download final publication PDF report
    """
    # Step 1: Scan image
    img_bytes = create_test_image(color=(230, 110, 25))
    scan_resp = client.post(
        "/api/v1/scans/predict",
        files={"file": ("carrot_peel_e2e.jpg", img_bytes, "image/jpeg")},
    )
    assert scan_resp.status_code == 200
    scan_data = scan_resp.json()
    scan_id = scan_data["scan_id"]
    assert scan_id > 0

    # Step 2: Confirm vegetable
    confirm_resp = client.post(
        "/api/v1/scans/confirm",
        json={
            "scan_id": scan_id,
            "confirmed_vegetable_id": 1,  # Carrot
            "confirmed_weight_grams": 200.0,
            "is_correction": False,
            "user_feedback_notes": "E2E automated validation test",
        },
    )
    assert confirm_resp.status_code in (200, 201)
    confirm_data = confirm_resp.json()
    assert confirm_data["confirmed_weight_grams"] == 200.0

    # Step 3: Run nutrient calculation
    est_resp = client.post(
        "/api/v1/nutrients/estimate",
        json={
            "vegetable_slug": "carrot",
            "input_weight_grams": 200.0,
            "input_weight_type": "whole",
            "preparation_method": "sauteed",
            "population_group": "adult_female",
            "servings": 1,
        },
    )
    assert est_resp.status_code == 200
    est_data = est_resp.json()
    assert est_data["vegetable_slug"] == "carrot"
    assert len(est_data["nutrients"]) > 0

    # Step 4: Safety evaluation
    safety_resp = client.post(
        "/api/v1/safety/evaluate",
        json={
            "vegetable_slug": "carrot",
            "conditions": {
                "is_green_or_sprouted": False,
                "is_bitter_tasting": False,
                "has_visible_mould": False,
                "is_unwashed": False,
            },
            "scan_confidence": 0.95,
        },
    )
    assert safety_resp.status_code == 200
    safety_data = safety_resp.json()
    assert safety_data["overall_safety_status"] == "safe_edible"
    assert safety_data["edible_recommendation_allowed"] is True

    # Step 5: Valorization recommendations
    reuse_resp = client.get("/api/v1/reuse/recommendations/carrot")
    assert reuse_resp.status_code == 200
    reuse_data = reuse_resp.json()
    assert len(reuse_data["recommendations"]) >= 1

    # Step 6: Log diverted waste
    waste_resp = client.post(
        "/api/v1/waste-tracking/log",
        json={
            "vegetable_slug": "carrot",
            "plant_part_code": "peel",
            "scan_id": scan_id,
            "weight_grams": est_data["calculated_peel_weight_grams"],
            "reuse_method_code": "aerobic_composting",
            "is_diverted": True,
            "notes": "E2E organic diversion test",
        },
    )
    assert waste_resp.status_code == 201
    waste_data = waste_resp.json()
    assert waste_data["weight_grams"] > 0

    # Step 7: Save archive report
    report_save_resp = client.post(
        "/api/v1/nutrients/reports/save",
        json={
            "confirmation_id": None,
            "vegetable_id": 1,
            "total_weight_grams": 200.0,
            "calculations": est_data,
            "safety_notes": safety_data,
            "user_feedback_notes": "E2E archive run",
        },
    )
    assert report_save_resp.status_code in (200, 201)
    report_data = report_save_resp.json()
    report_uuid = report_data["report_uuid"]
    assert report_uuid.startswith("RPT-")

    # Step 8: Download final PDF report
    pdf_resp = client.get(f"/api/v1/nutrients/reports/{report_uuid}/pdf")
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
    assert pdf_resp.content.startswith(b"%PDF-")
    assert len(pdf_resp.content) > 1500
