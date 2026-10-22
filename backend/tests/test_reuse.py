import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_reuse_methods():
    response = client.get("/api/v1/reuse/methods")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 8
    codes = [m["code"] for m in data]
    assert "aerobic_composting" in codes
    assert "vermicomposting" in codes
    assert "biogas_anaerobic" in codes
    assert "culinary_stock" in codes
    assert "natural_pigment" in codes


def test_list_reuse_methods_filtered_by_category():
    response = client.get("/api/v1/reuse/methods?category=composting")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    for m in data:
        assert m["category"] == "composting"


def test_list_reuse_categories():
    response = client.get("/api/v1/reuse/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
    categories = [c["category"] for c in data]
    assert "food" in categories
    assert "composting" in categories
    assert "biogas" in categories


def test_get_carrot_reuse_recommendations():
    response = client.get("/api/v1/reuse/recommendations/carrot")
    assert response.status_code == 200
    data = response.json()
    assert data["vegetable_slug"] == "carrot"
    assert data["edible_culinary_allowed"] is True
    assert data["total_recommendations"] >= 3

    # Check evidence rank ordering
    ranks = [r["evidence_rank"] for r in data["recommendations"]]
    assert ranks == sorted(ranks)

    # Contains food and pigment extraction
    categories = [r["category"] for r in data["recommendations"]]
    assert "food" in categories
    assert "pigment_extraction" in categories
    assert "composting" in categories


def test_get_cassava_reuse_recommendations_inhibits_food_use():
    response = client.get("/api/v1/reuse/recommendations/cassava-tapioca")
    assert response.status_code == 200
    data = response.json()
    assert data["vegetable_slug"] == "cassava-tapioca"
    assert data["edible_culinary_allowed"] is False

    # Strictly verify zero food recommendations are returned for hazardous cassava peel
    for rec in data["recommendations"]:
        assert rec["category"] != "food", "Cassava peels must never have culinary recommendations!"

    categories = [r["category"] for r in data["recommendations"]]
    assert "biogas" in categories or "composting" in categories


def test_get_reuse_recommendations_non_existent_vegetable():
    response = client.get("/api/v1/reuse/recommendations/invalid_peel_name")
    assert response.status_code == 404


def test_list_meaningful_creations_all():
    response = client.get("/api/v1/reuse/creations")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 10
    assert len(data["creations"]) >= 10
    assert "eco_home" in data["categories"]
    assert "garden_soil" in data["categories"]
    assert "arts_crafts" in data["categories"]
    assert "culinary_gourmet" in data["categories"]

    ids = [c["id"] for c in data["creations"]]
    assert "bio_enzyme_cleaner" in ids
    assert "biodegradable_seedling_pots" in ids
    assert "cold_steeped_peel_tea" in ids
    assert "beetroot_botanical_watercolors" in ids
    assert "zero_waste_veggie_bouillon" in ids


def test_list_meaningful_creations_filtered_by_category():
    response = client.get("/api/v1/reuse/creations?category=eco_home")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2
    for c in data["creations"]:
        assert c["category"] == "eco_home"


def test_list_meaningful_creations_filtered_by_vegetable():
    response = client.get("/api/v1/reuse/creations?vegetable_slug=beetroot")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    ids = [c["id"] for c in data["creations"]]
    assert "beetroot_botanical_watercolors" in ids


def test_get_meaningful_creation_detail_success():
    response = client.get("/api/v1/reuse/creations/bio_enzyme_cleaner")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "bio_enzyme_cleaner"
    assert "Citrus" in data["title_en"]
    assert len(data["required_materials_en"]) >= 3
    assert len(data["step_by_step_instructions_en"]) >= 5
    assert "safety_and_storage_en" in data


def test_get_meaningful_creation_detail_not_found():
    response = client.get("/api/v1/reuse/creations/unknown_creation_xyz")
    assert response.status_code == 404

