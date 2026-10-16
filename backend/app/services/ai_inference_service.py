import io
import json
import logging
from pathlib import Path
from typing import Dict, Any, List

from PIL import Image, UnidentifiedImageError
import torch
import torch.nn as nn
from torchvision import models, transforms

logger = logging.getLogger("smart_peel_ai_inference")

AI_DIR = Path(__file__).resolve().parent.parent.parent.parent / "ai"
MODEL_PATH = AI_DIR / "models" / "smart_peel_mobilenetv3.pt"
LABELS_PATH = AI_DIR / "models" / "class_labels.json"


class AIInferenceService:
    _instance = None
    _model = None
    _metadata = None
    _transform = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIInferenceService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        logger.info("Initializing AI Inference Service...")
        if not LABELS_PATH.exists():
            raise FileNotFoundError(f"Class labels not found at {LABELS_PATH}")

        with open(LABELS_PATH, "r", encoding="utf-8") as f:
            self._metadata = json.load(f)

        num_classes = len(self._metadata["classes"])
        self._model = models.mobilenet_v3_small(weights=None)
        in_features = self._model.classifier[3].in_features
        self._model.classifier[3] = nn.Sequential(
            nn.Dropout(p=0.2),
            nn.Linear(in_features, num_classes),
        )

        if MODEL_PATH.exists():
            checkpoint = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
            if "model_state_dict" in checkpoint:
                self._model.load_state_dict(checkpoint["model_state_dict"])
            else:
                self._model.load_state_dict(checkpoint)
            logger.info("Loaded MobileNetV3 weights successfully.")
        else:
            logger.warning(f"Model file {MODEL_PATH} not found; model is uninitialized.")

        self._model.eval()

        self._transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=self._metadata["normalization"]["mean"],
                    std=self._metadata["normalization"]["std"],
                ),
            ]
        )

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata

    def predict_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Takes raw image bytes, validates format, runs inference,
        and returns prediction rankings with confidence scores.
        """
        if not image_bytes or len(image_bytes) == 0:
            raise ValueError("Empty image payload provided.")

        try:
            image = Image.open(io.BytesIO(image_bytes))
            image = image.convert("RGB")
        except (UnidentifiedImageError, OSError) as e:
            raise ValueError(f"Invalid or corrupted image format: {e}")

        tensor = self._transform(image).unsqueeze(0)

        with torch.no_grad():
            logits = self._model(tensor)
            probs = torch.softmax(logits, dim=1).squeeze(0)

        confidence_threshold = self._metadata.get("confidence_threshold", 0.65)
        classes = self._metadata["classes"]

        # Rank predictions by probability descending
        sorted_indices = torch.argsort(probs, descending=True).tolist()
        top_predictions: List[Dict[str, Any]] = []

        for idx in sorted_indices:
            cls_info = classes[idx]
            conf = float(probs[idx].item())
            top_predictions.append(
                {
                    "class_key": cls_info["key"],
                    "slug": cls_info["slug"],
                    "confidence": round(conf, 4),
                    "display_name_en": cls_info["displayNameEn"],
                    "display_name_ta": cls_info["displayNameTa"],
                    "scientific_name": cls_info["scientificName"],
                    "is_supported_peel": cls_info["isSupportedPeel"],
                }
            )

        top_pred = top_predictions[0]
        top_conf = top_pred["confidence"]
        is_supported = top_pred["is_supported_peel"]

        is_uncertain = top_conf < confidence_threshold or not is_supported
        confirmation_required = True

        safety_notice = (
            "Visual identification is probabilistic. Always verify the vegetable peel before "
            "preparation, and never rely on computer vision alone for food safety compliance."
        )

        return {
            "predicted_vegetable_slug": top_pred["slug"] if is_supported else None,
            "predicted_display_name_en": top_pred["display_name_en"],
            "predicted_display_name_ta": top_pred["display_name_ta"],
            "predicted_plant_part": "Peel / தோல்",
            "confidence": top_conf,
            "model_version": self._metadata.get("version", "1.0.0"),
            "is_supported_peel": is_supported and (top_conf >= confidence_threshold),
            "confirmation_required": confirmation_required,
            "is_uncertain": is_uncertain,
            "top_predictions": top_predictions,
            "safety_notice": safety_notice,
        }


ai_inference_service = AIInferenceService()
