# AI MODEL CARD — SMART PEEL MOBILENETV3

## 1. Model Details
- **Model Name**: Smart Peel MobileNetV3 Classifier
- **Model Version**: v1.0.0-mobilenetv3
- **Base Architecture**: MobileNetV3-Small (Torchvision)
- **Pretrained Weights**: ImageNet-1K transferred
- **Custom Classifier Head**: Dropout(0.2) + Linear(1024 -> 6 classes)
- **File Format**: PyTorch Checkpoint (`smart_peel_mobilenetv3.pt`, 5.94 MB)
- **Inference Latency**: ~35ms on CPU, ~8ms on GPU

---

## 2. Intended Use
- **Primary Task**: Image-based classification of vegetable peels into supported botanical categories or rejection as unsupported/non-peel objects.
- **Intended Users**: Households, commercial kitchens, food processing units, agricultural researchers.
- **Out of Scope**: Direct laboratory-grade chemical identification. Output is strictly probabilistic and requires human-in-the-loop confirmation before nutritional consumption.

---

## 3. Training & Validation Dataset
- **Total Images**: 360 stratified images (60 images/class across 6 classes).
- **Classes**:
  1. `carrot_peel` (*Daucus carota subsp. sativus*)
  2. `potato_peel` (*Solanum tuberosum*)
  3. `beetroot_peel` (*Beta vulgaris*)
  4. `cucumber_peel` (*Cucumis sativus*)
  5. `pumpkin_peel` (*Cucurbita moschata*)
  6. `unsupported_object` (Negative background class for outlier rejection)
- **Split Ratio**: 70% Train (252 images), 15% Validation (54 images), 15% Test (54 images).
- **Data Augmentations**: Random horizontal/vertical flip, random rotation (+/- 25 deg), color jitter (brightness, contrast, saturation), affine translation.

---

## 4. Evaluation Metrics

| Metric | Result |
|---|---|
| **Test Accuracy** | **100.0%** (54/54 test samples) |
| **Macro Precision** | **1.0000** |
| **Macro Recall** | **1.0000** |
| **Macro F1-Score** | **1.0000** |
| **Unsupported Class Rejection Rate** | **100.0%** (9/9 negative controls rejected) |

---

## 5. Decision & Rejection Boundary
- **Confidence Threshold**: 65.0% (`CONFIDENCE_THRESHOLD = 0.65`).
- **Uncertainty Flag**: If top-1 prediction confidence < 0.65 OR top class is `unsupported_object`, the system marks `is_uncertain = True` and flags the scan as unsupported or requiring manual vegetable selection.
- **Safety Policy**: Visual identification never overrides chemical safety warnings.
