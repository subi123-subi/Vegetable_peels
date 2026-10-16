import io
from pathlib import Path
from PIL import Image
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

AI_DIR = Path(__file__).resolve().parent.parent.parent / "ai"
TEST_DATA_DIR = AI_DIR / "datasets" / "processed" / "test"


def create_test_image_bytes(color=(230, 81, 0), format="JPEG"):
    buf = io.BytesIO()
    img = Image.new("RGB", (224, 224), color=color)
    img.save(buf, format=format)
    return buf.getvalue()


def test_get_active_model_info():
    response = client.get("/api/v1/scans/models/active")
    assert response.status_code == 200
    data = response.json()
    assert data["architecture"] == "MobileNetV3-Small"
    assert data["classes_count"] == 6
    assert data["confidence_threshold"] == 0.65
    assert len(data["classes"]) == 6


def test_predict_scan_valid_carrot_image():
    # Use real test image if available, else synthetic
    carrot_images = list((TEST_DATA_DIR / "carrot_peel").glob("*.jpg"))
    if carrot_images:
        with open(carrot_images[0], "rb") as f:
            image_bytes = f.read()
    else:
        image_bytes = create_test_image_bytes(color=(239, 108, 0))

    files = {"file": ("test_carrot.jpg", image_bytes, "image/jpeg")}
    response = client.post("/api/v1/scans/predict", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["scan_id"] > 0
    assert data["prediction_id"] > 0
    assert data["predicted_vegetable_slug"] == "carrot"
    assert data["is_supported_peel"] is True
    assert data["confidence"] >= 0.65
    assert data["confirmation_required"] is True
    assert len(data["top_predictions"]) == 6
    assert "safety_notice" in data


def test_predict_scan_unsupported_object_rejected():
    unsupported_images = list((TEST_DATA_DIR / "unsupported_object").glob("*.jpg"))
    if unsupported_images:
        with open(unsupported_images[0], "rb") as f:
            image_bytes = f.read()
    else:
        image_bytes = create_test_image_bytes(color=(33, 150, 243))

    files = {"file": ("unsupported_test.jpg", image_bytes, "image/jpeg")}
    response = client.post("/api/v1/scans/predict", files=files)

    assert response.status_code == 200
    data = response.json()
    # Should flag as unsupported or uncertain
    assert data["is_supported_peel"] is False
    assert data["is_uncertain"] is True
    assert data["predicted_vegetable_slug"] is None


def test_predict_scan_empty_file_rejected():
    files = {"file": ("empty.jpg", b"", "image/jpeg")}
    response = client.post("/api/v1/scans/predict", files=files)
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_predict_scan_corrupt_file_rejected():
    files = {"file": ("corrupt.jpg", b"NOT_A_REAL_IMAGE_DATA_BYTES", "image/jpeg")}
    response = client.post("/api/v1/scans/predict", files=files)
    assert response.status_code == 400
    assert "image decoding failed" in response.json()["detail"].lower()


def test_predict_scan_invalid_mime_type_rejected():
    files = {"file": ("document.pdf", b"%PDF-1.4...", "application/pdf")}
    response = client.post("/api/v1/scans/predict", files=files)
    assert response.status_code == 400
    assert "unsupported file format" in response.json()["detail"].lower()


def test_confirm_scan_success():
    # 1. Create a scan prediction first
    image_bytes = create_test_image_bytes(color=(239, 108, 0))
    files = {"file": ("scan_for_confirm.jpg", image_bytes, "image/jpeg")}
    pred_res = client.post("/api/v1/scans/predict", files=files)
    assert pred_res.status_code == 200
    scan_id = pred_res.json()["scan_id"]

    # 2. Confirm as carrot (vegetable ID 1 or query carrot)
    veg_res = client.get("/api/v1/vegetables/carrot")
    assert veg_res.status_code == 200
    carrot_id = veg_res.json()["id"]

    confirm_payload = {
        "scan_id": scan_id,
        "confirmed_vegetable_id": carrot_id,
        "confirmed_weight_grams": 150.0,
        "is_correction": False,
        "user_feedback_notes": "Confirmed carrot peel from home cooking.",
    }

    res = client.post("/api/v1/scans/confirm", json=confirm_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["scan_id"] == scan_id
    assert data["confirmed_vegetable_id"] == carrot_id
    assert data["confirmed_weight_grams"] == 150.0
    assert data["is_correction"] is False


def test_confirm_scan_non_existent_scan():
    payload = {
        "scan_id": 999999,
        "confirmed_vegetable_id": 1,
        "confirmed_weight_grams": 100.0,
    }
    res = client.post("/api/v1/scans/confirm", json=payload)
    assert res.status_code == 404
    assert "scan record not found" in res.json()["detail"].lower()
