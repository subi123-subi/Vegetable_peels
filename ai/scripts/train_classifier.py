"""
MobileNetV3 Vegetable Peel Image Classifier Training & Evaluation Pipeline
Phase 7 — AI Model Development for Smart Peel AI
"""

import json
import logging
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import classification_report, confusion_matrix
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("smart_peel_ai_trainer")

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "datasets" / "processed"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Hyperparameters
NUM_CLASSES = 6
BATCH_SIZE = 16
NUM_EPOCHS = 12
LEARNING_RATE = 1e-3
IMAGE_SIZE = 224
CONFIDENCE_THRESHOLD = 0.65

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CLASS_METADATA = {
    "beetroot_peel": {
        "slug": "beetroot",
        "name_en": "Beetroot Peel",
        "name_ta": "பீட்ரூட் தோல்",
        "scientific_name": "Beta vulgaris",
    },
    "carrot_peel": {
        "slug": "carrot",
        "name_en": "Carrot Peel",
        "name_ta": "கேரட் தோல்",
        "scientific_name": "Daucus carota subsp. sativus",
    },
    "cucumber_peel": {
        "slug": "cucumber",
        "name_en": "Cucumber Peel",
        "name_ta": "வெள்ளரி தோல்",
        "scientific_name": "Cucumis sativus",
    },
    "potato_peel": {
        "slug": "potato",
        "name_en": "Potato Peel",
        "name_ta": "உருளைக்கிழங்கு தோல்",
        "scientific_name": "Solanum tuberosum",
    },
    "pumpkin_peel": {
        "slug": "pumpkin",
        "name_en": "Pumpkin Peel",
        "name_ta": "பூசணிக்காய் தோல்",
        "scientific_name": "Cucurbita moschata",
    },
    "unsupported_object": {
        "slug": "unsupported",
        "name_en": "Unsupported / Non-peel Object",
        "name_ta": "ஆதரிக்கப்படாத பொருள்",
        "scientific_name": "N/A",
    },
}


def get_data_loaders():
    train_transform = transforms.Compose(
        [
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=20),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
            ),
        ]
    )

    val_test_transform = transforms.Compose(
        [
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
            ),
        ]
    )

    train_dataset = datasets.ImageFolder(
        DATA_DIR / "train", transform=train_transform
    )
    val_dataset = datasets.ImageFolder(
        DATA_DIR / "val", transform=val_test_transform
    )
    test_dataset = datasets.ImageFolder(
        DATA_DIR / "test", transform=val_test_transform
    )

    train_loader = DataLoader(
        train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0
    )
    val_loader = DataLoader(
        val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0
    )
    test_loader = DataLoader(
        test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=0
    )

    return train_loader, val_loader, test_loader, train_dataset.classes


def build_model(num_classes: int):
    logger.info("Initializing MobileNetV3-Small architecture...")
    try:
        model = models.mobilenet_v3_small(
            weights=models.MobileNet_V3_Small_Weights.DEFAULT
        )
        logger.info("Loaded pretrained MobileNetV3 weights successfully.")
    except Exception as e:
        logger.warning(
            f"Could not download online weights ({e}); initializing without pretrained weights."
        )
        model = models.mobilenet_v3_small(weights=None)

    # Replace classifier head for transfer learning
    in_features = model.classifier[3].in_features
    model.classifier[3] = nn.Sequential(
        nn.Dropout(p=0.2),
        nn.Linear(in_features, num_classes),
    )
    return model.to(DEVICE)


def train_model(model, train_loader, val_loader, num_epochs=NUM_EPOCHS):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=LEARNING_RATE, weight_decay=1e-4
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=num_epochs
    )

    best_val_acc = 0.0
    best_weights = None

    logger.info(f"Starting training on device: {DEVICE} for {num_epochs} epochs...")
    start_time = time.time()

    for epoch in range(1, num_epochs + 1):
        # Training Phase
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0

        for images, labels in train_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct_train += torch.sum(preds == labels.data).item()
            total_train += labels.size(0)

        scheduler.step()
        train_loss = running_loss / total_train
        train_acc = correct_train / total_train

        # Validation Phase
        model.eval()
        val_loss = 0.0
        correct_val = 0
        total_val = 0

        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(DEVICE), labels.to(DEVICE)
                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                correct_val += torch.sum(preds == labels.data).item()
                total_val += labels.size(0)

        val_loss = val_loss / total_val
        val_acc = correct_val / total_val

        logger.info(
            f"Epoch {epoch:02d}/{num_epochs:02d} - "
            f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f} | "
            f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}"
        )

        if val_acc >= best_val_acc:
            best_val_acc = val_acc
            best_weights = model.state_dict().copy()

    elapsed = time.time() - start_time
    logger.info(
        f"Training completed in {elapsed:.1f}s. Best Val Accuracy: {best_val_acc:.4f}"
    )

    if best_weights is not None:
        model.load_state_dict(best_weights)

    return model, best_val_acc


def evaluate_model(model, test_loader, class_names):
    logger.info("Evaluating on held-out test dataset...")
    model.eval()

    all_preds = []
    all_labels = []
    all_probs = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(DEVICE)
            outputs = model(images)
            probs = torch.softmax(outputs, dim=1)
            max_probs, preds = torch.max(probs, dim=1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())
            all_probs.extend(max_probs.cpu().numpy())

    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    all_probs = np.array(all_probs)

    test_acc = np.mean(all_preds == all_labels)
    report_dict = classification_report(
        all_labels,
        all_preds,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )
    cm = confusion_matrix(all_labels, all_preds)

    # Rejection analysis for unsupported/uncertain samples
    unsupported_idx = class_names.index("unsupported_object")
    unsupported_mask = all_labels == unsupported_idx
    unsupported_acc = np.mean(all_preds[unsupported_mask] == unsupported_idx)

    # Low confidence rejection rate
    low_conf_mask = all_probs < CONFIDENCE_THRESHOLD
    rejected_count = int(np.sum(low_conf_mask))

    logger.info("================ EVALUATION SUMMARY ================")
    logger.info(f"Test Accuracy: {test_acc:.4f}")
    logger.info(
        f"Macro F1-Score: {report_dict['macro avg']['f1-score']:.4f}"
    )
    logger.info(f"Unsupported Object Rejection Rate: {unsupported_acc:.4f}")
    logger.info(
        f"Low-Confidence Rejections (< {CONFIDENCE_THRESHOLD}): {rejected_count}/{len(all_labels)}"
    )

    return {
        "test_accuracy": float(test_acc),
        "macro_precision": float(report_dict["macro avg"]["precision"]),
        "macro_recall": float(report_dict["macro avg"]["recall"]),
        "macro_f1": float(report_dict["macro avg"]["f1-score"]),
        "unsupported_accuracy": float(unsupported_acc),
        "confidence_threshold": CONFIDENCE_THRESHOLD,
        "classification_report": report_dict,
        "confusion_matrix": cm.tolist(),
        "total_test_samples": len(all_labels),
    }


def export_artifacts(model, class_names, metrics):
    # Save Model Weights
    pt_path = MODEL_DIR / "smart_peel_mobilenetv3.pt"
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "class_names": class_names,
            "architecture": "MobileNetV3-Small",
            "version": "1.0.0",
            "input_resolution": [IMAGE_SIZE, IMAGE_SIZE, 3],
            "confidence_threshold": CONFIDENCE_THRESHOLD,
        },
        pt_path,
    )
    logger.info(f"Exported PyTorch model checkpoint to {pt_path}")

    # Save Class Labels and Metadata
    class_mapping = {
        "version": "1.0.0",
        "model_architecture": "MobileNetV3-Small",
        "input_resolution": [IMAGE_SIZE, IMAGE_SIZE, 3],
        "normalization": {
            "mean": [0.485, 0.456, 0.406],
            "std": [0.229, 0.224, 0.225],
        },
        "confidence_threshold": CONFIDENCE_THRESHOLD,
        "classes": [],
    }

    for idx, name in enumerate(class_names):
        meta = CLASS_METADATA.get(
            name,
            {
                "slug": name,
                "name_en": name.replace("_", " ").title(),
                "name_ta": name,
                "scientific_name": "N/A",
            },
        )
        class_mapping["classes"].append(
            {
                "index": idx,
                "key": name,
                "slug": meta["slug"],
                "displayNameEn": meta["name_en"],
                "displayNameTa": meta["name_ta"],
                "scientificName": meta["scientific_name"],
                "isSupportedPeel": name != "unsupported_object",
            }
        )

    labels_path = MODEL_DIR / "class_labels.json"
    with open(labels_path, "w", encoding="utf-8") as f:
        json.dump(class_mapping, f, indent=2, ensure_ascii=False)
    logger.info(f"Exported class mapping and metadata to {labels_path}")

    # Save Evaluation Metrics
    metrics_path = MODEL_DIR / "model_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    logger.info(f"Exported evaluation metrics to {metrics_path}")


def main():
    logger.info("=== SMART PEEL AI — MobileNetV3 Training Pipeline ===")
    train_loader, val_loader, test_loader, class_names = get_data_loaders()
    logger.info(f"Classes ({len(class_names)}): {class_names}")

    model = build_model(num_classes=len(class_names))
    model, best_val_acc = train_model(
        model, train_loader, val_loader, num_epochs=NUM_EPOCHS
    )

    metrics = evaluate_model(model, test_loader, class_names)
    metrics["best_val_accuracy"] = float(best_val_acc)
    metrics["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

    export_artifacts(model, class_names, metrics)
    logger.info("Phase 7 Model Development pipeline completed successfully.")


if __name__ == "__main__":
    main()
