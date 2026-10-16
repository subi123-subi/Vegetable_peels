import json
from pathlib import Path
import torch
import torch.nn as nn
from torchvision import models
from PIL import Image
import torchvision.transforms as transforms

AI_DIR = Path(__file__).resolve().parent.parent.parent / "ai"
MODEL_PATH = AI_DIR / "models" / "smart_peel_mobilenetv3.pt"
LABELS_PATH = AI_DIR / "models" / "class_labels.json"
METRICS_PATH = AI_DIR / "models" / "model_metrics.json"
TEST_DATA_DIR = AI_DIR / "datasets" / "processed" / "test"


def test_model_artifacts_exist():
    assert MODEL_PATH.exists(), "Trained model checkpoint smart_peel_mobilenetv3.pt must exist"
    assert LABELS_PATH.exists(), "class_labels.json must exist"
    assert METRICS_PATH.exists(), "model_metrics.json must exist"


def test_class_labels_metadata():
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)

    assert meta["version"] == "1.0.0"
    assert meta["model_architecture"] == "MobileNetV3-Small"
    assert meta["confidence_threshold"] == 0.65
    assert len(meta["classes"]) == 6

    # Verify Tamil and English names exist for all classes
    for cls in meta["classes"]:
        assert "displayNameEn" in cls and len(cls["displayNameEn"]) > 0
        assert "displayNameTa" in cls and len(cls["displayNameTa"]) > 0
        assert "isSupportedPeel" in cls


def test_model_metrics_standards():
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    assert metrics["test_accuracy"] >= 0.85
    assert metrics["macro_f1"] >= 0.85
    assert metrics["unsupported_accuracy"] >= 0.85
    assert len(metrics["confusion_matrix"]) == 6


def test_model_forward_pass_and_inference():
    checkpoint = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
    assert "model_state_dict" in checkpoint

    model = models.mobilenet_v3_small(weights=None)
    in_features = model.classifier[3].in_features
    model.classifier[3] = nn.Sequential(
        nn.Dropout(p=0.2),
        nn.Linear(in_features, 6),
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    # Synthetic tensor forward pass
    dummy_input = torch.randn(1, 3, 224, 224)
    with torch.no_grad():
        output = model(dummy_input)
    assert output.shape == (1, 6)

    probs = torch.softmax(output, dim=1)
    assert torch.isclose(probs.sum(), torch.tensor(1.0), atol=1e-4)

    # Real test image inference
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    sample_carrot = next((TEST_DATA_DIR / "carrot_peel").glob("*.jpg"))
    img = Image.open(sample_carrot).convert("RGB")
    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        pred_logits = model(tensor)
        pred_probs = torch.softmax(pred_logits, dim=1)
        pred_idx = torch.argmax(pred_probs, dim=1).item()

    assert checkpoint["class_names"][pred_idx] == "carrot_peel"
    assert pred_probs[0][pred_idx].item() >= 0.65
