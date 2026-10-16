import json
from pathlib import Path
from PIL import Image

AI_DIR = Path(__file__).resolve().parent.parent.parent / "ai"
DATASET_DIR = AI_DIR / "datasets" / "processed"
SUMMARY_FILE = DATASET_DIR / "dataset_summary.json"


def test_dataset_summary_exists_and_valid():
    """Verify dataset summary metadata exists and adheres to schema."""
    assert SUMMARY_FILE.exists(), "dataset_summary.json must exist in ai/datasets/processed"
    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "classes" in data
    assert len(data["classes"]) == 6
    expected_classes = [
        "carrot_peel",
        "potato_peel",
        "beetroot_peel",
        "cucumber_peel",
        "pumpkin_peel",
        "unsupported_object",
    ]
    assert data["classes"] == expected_classes
    assert data["total_images"] == 360
    assert data["input_resolution"] == [224, 224, 3]
    assert "splits" in data
    assert set(data["splits"].keys()) == {"train", "val", "test"}


def test_dataset_split_directories_and_files():
    """Verify all split folders and image files exist and are valid readable images."""
    assert DATASET_DIR.exists()
    for split in ["train", "val", "test"]:
        split_dir = DATASET_DIR / split
        assert split_dir.exists(), f"Split directory {split} must exist"

        classes = [d.name for d in split_dir.iterdir() if d.is_dir()]
        assert len(classes) == 6, f"Split {split} must contain all 6 class subfolders"

        for cls in classes:
            cls_dir = split_dir / cls
            images = list(cls_dir.glob("*.jpg"))
            assert len(images) > 0, f"Class directory {cls_dir} must not be empty"

            # Check first image in each class for valid resolution and format
            sample_img = images[0]
            with Image.open(sample_img) as img:
                assert img.format == "JPEG"
                assert img.size == (224, 224)
                assert img.mode == "RGB"
