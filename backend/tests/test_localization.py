import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.models.vegetable import Vegetable, PlantPart
from app.models.reuse import ReuseMethod, ReuseRecommendation
from app.models.safety import SafetyRule


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_translations_dictionary_english(client):
    """Test retrieval of English translation dictionary."""
    resp = client.get("/api/v1/translations/dictionary?lang=en")
    assert resp.status_code == 200
    data = resp.json()
    assert data["language_code"] == "en"
    trans = data["translations"]
    assert "app_name" in trans
    assert trans["app_name"] == "SMART PEEL AI"
    assert "scientific_disclaimer" in trans
    assert "solanine_warning" in trans


def test_translations_dictionary_tamil(client):
    """Test retrieval of Tamil translation dictionary with UTF-8 characters."""
    resp = client.get("/api/v1/translations/dictionary?lang=ta")
    assert resp.status_code == 200
    data = resp.json()
    assert data["language_code"] == "ta"
    trans = data["translations"]
    assert "app_name" in trans
    # Verify presence of Tamil characters
    assert any(ord(c) >= 0x0B80 and ord(c) <= 0x0BFF for c in trans["app_name"])
    assert "scientific_disclaimer" in trans
    assert any(ord(c) >= 0x0B80 and ord(c) <= 0x0BFF for c in trans["scientific_disclaimer"])


def test_seed_and_create_translation(client):
    """Test translation seeding and single key creation/update."""
    # Seed
    seed_resp = client.post("/api/v1/translations/seed")
    assert seed_resp.status_code == 200
    assert seed_resp.json()["status"] == "success"

    # Create new
    post_resp = client.post(
        "/api/v1/translations/",
        json={
            "translation_key": "test_phase_18_key",
            "language_code": "ta",
            "translated_text": "சோதனை உரை",
            "context": "test",
        },
    )
    assert post_resp.status_code == 201
    assert post_resp.json()["translation_key"] == "test_phase_18_key"

    # Query back
    get_resp = client.get("/api/v1/translations/dictionary?lang=ta")
    assert get_resp.status_code == 200
    assert "test_phase_18_key" in get_resp.json()["translations"]


def test_all_50_vegetables_have_tamil_names():
    """Verify that all 50 botanical vegetables have valid, non-empty Tamil names."""
    db = SessionLocal()
    try:
        vegetables = db.query(Vegetable).all()
        assert len(vegetables) >= 50, f"Expected at least 50 vegetables, found {len(vegetables)}"
        for veg in vegetables:
            assert veg.name_en and len(veg.name_en.strip()) > 0, f"Missing name_en for {veg.slug}"
            assert veg.name_ta and len(veg.name_ta.strip()) > 0, f"Missing name_ta for {veg.slug}"
            # Check for Tamil Unicode block range: U+0B80 to U+0BFF
            has_tamil_chars = any(0x0B80 <= ord(c) <= 0x0BFF for c in veg.name_ta)
            assert has_tamil_chars, f"name_ta for {veg.slug} ('{veg.name_ta}') has no Tamil characters"
    finally:
        db.close()


def test_all_plant_parts_have_tamil_names():
    """Verify that all plant parts have valid Tamil representations."""
    db = SessionLocal()
    try:
        parts = db.query(PlantPart).all()
        assert len(parts) >= 1
        for p in parts:
            assert p.name_en and len(p.name_en.strip()) > 0
            assert p.name_ta and len(p.name_ta.strip()) > 0
            has_tamil_chars = any(0x0B80 <= ord(c) <= 0x0BFF for c in p.name_ta)
            assert has_tamil_chars, f"PlantPart {p.name_en} missing Tamil translation"
    finally:
        db.close()


def test_all_reuse_methods_and_recommendations_have_tamil():
    """Verify that valorization methods and instructions have Tamil translations."""
    db = SessionLocal()
    try:
        methods = db.query(ReuseMethod).all()
        assert len(methods) >= 4
        for m in methods:
            assert m.name_ta and len(m.name_ta.strip()) > 0

        recs = db.query(ReuseRecommendation).all()
        assert len(recs) >= 50
        for r in recs:
            assert r.preparation_instructions_ta and len(r.preparation_instructions_ta.strip()) > 0
    finally:
        db.close()


def test_all_safety_rules_have_tamil_hazards():
    """Verify that all food safety rules have localized Tamil alerts."""
    db = SessionLocal()
    try:
        rules = db.query(SafetyRule).all()
        assert len(rules) >= 4
        for rule in rules:
            assert rule.rule_description_ta and len(rule.rule_description_ta.strip()) > 0
            has_tamil_chars = any(0x0B80 <= ord(c) <= 0x0BFF for c in rule.rule_description_ta)
            assert has_tamil_chars, f"SafetyRule {rule.code} rule_description_ta has no Tamil characters"
    finally:
        db.close()
