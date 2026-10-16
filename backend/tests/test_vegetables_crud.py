import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_vegetables_default():
    response = client.get("/api/v1/vegetables/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert data["total"] >= 50
    assert len(data["items"]) <= 50
    assert data["items"][0]["name_en"] != ""
    assert data["items"][0]["name_ta"] != ""


def test_list_vegetables_all():
    response = client.get("/api/v1/vegetables/?all=true")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 50
    assert len(data["items"]) >= 50


def test_list_vegetables_filter_ai():
    response = client.get("/api/v1/vegetables/?is_ai_supported=true")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 5
    for item in data["items"]:
        assert item["is_ai_supported"] is True
        assert item["ai_class_name"] is not None


def test_list_vegetables_search_english():
    response = client.get("/api/v1/vegetables/?search=carrot")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    slugs = [v["slug"] for v in data["items"]]
    assert "carrot" in slugs


def test_list_vegetables_search_scientific():
    response = client.get("/api/v1/vegetables/?search=Solanum")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 2  # Potato, Brinjal, etc.


def test_get_categories_list():
    response = client.get("/api/v1/vegetables/categories")
    assert response.status_code == 200
    categories = response.json()
    assert len(categories) >= 4
    cat_names = [c["category"] for c in categories]
    assert any("Root" in c for c in cat_names)


def test_get_plant_parts_list():
    response = client.get("/api/v1/vegetables/plant-parts")
    assert response.status_code == 200
    parts = response.json()
    assert len(parts) >= 7
    codes = [p["code"] for p in parts]
    assert "peel" in codes
    assert "rind" in codes
    assert "outer_leaves" in codes


def test_get_vegetable_detail_carrot():
    response = client.get("/api/v1/vegetables/carrot")
    assert response.status_code == 200
    veg = response.json()
    assert veg["slug"] == "carrot"
    assert veg["name_en"] == "Carrot"
    assert veg["is_ai_supported"] is True
    assert veg["ai_class_name"] == "carrot_peel"
    assert len(veg["nutrients"]) >= 5
    nutrient_codes = [n["nutrient_code"] for n in veg["nutrients"]]
    assert "vit_a" in nutrient_codes
    assert "calcium" in nutrient_codes


def test_get_vegetable_detail_potato_safety():
    response = client.get("/api/v1/vegetables/potato")
    assert response.status_code == 200
    veg = response.json()
    assert veg["slug"] == "potato"
    assert len(veg["safety_rules"]) >= 1
    assert any(r["hazard_type"] == "glycoalkaloid" for r in veg["safety_rules"])


def test_get_nonexistent_vegetable():
    response = client.get("/api/v1/vegetables/nonexistent-dragonfruit")
    assert response.status_code == 404


def test_create_update_delete_vegetable_crud():
    # 1. Create a test vegetable
    payload = {
        "slug": "test-ash-gourd-sample",
        "name_en": "Test Ash Gourd",
        "name_ta": "சோதனை சாம்பல் பூசணி",
        "scientific_name": "Benincasa hispida test",
        "category": "Gourds & Cucurbits",
        "plant_part_id": 3,  # rind
        "is_ai_supported": False,
        "nutrient_data_status": "incomplete",
        "food_safety_status": "safe_edible",
    }
    create_res = client.post("/api/v1/vegetables/", json=payload)
    assert create_res.status_code == 201
    created_id = create_res.json()["id"]

    # 2. Reject duplicate slug
    dup_res = client.post("/api/v1/vegetables/", json=payload)
    assert dup_res.status_code == 400

    # 3. Update vegetable
    update_res = client.put(f"/api/v1/vegetables/{created_id}", json={"name_en": "Updated Test Gourd"})
    assert update_res.status_code == 200
    assert update_res.json()["name_en"] == "Updated Test Gourd"

    # 4. Delete vegetable (permanent)
    del_res = client.delete(f"/api/v1/vegetables/{created_id}?permanent=true")
    assert del_res.status_code == 200

    # 5. Verify deleted
    get_res = client.get(f"/api/v1/vegetables/{created_id}")
    assert get_res.status_code == 404
