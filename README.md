# SMART PEEL AI — Intelligent Vegetable Peel Nutrient Identification and Food Waste Valorization System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Flutter](https://img.shields.io/badge/Flutter-3.47+-02569B.svg?logo=flutter&logoColor=white)](https://flutter.dev)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![Tests Passing](https://img.shields.io/badge/Tests-105%20Backend%20%7C%2013%20Frontend%20Passed-brightgreen.svg)]()
[![Code Quality](https://img.shields.io/badge/Flutter%20Analyze-0%20Issues-brightgreen.svg)]()
[![Bilingual](https://img.shields.io/badge/Language-English%20%7C%20%E0%AE%A4%E0%AE%AE%E0%AE%BF%E0%AE%B4%E0%AF%8D-blue.svg)]()

**SMART PEEL AI** is a production-grade, scientifically responsible software application designed to identify vegetable peels from photographs, quantify their nutritional composition, enforce strict food safety rules, and recommend evidence-ranked waste valorization strategies (including culinary preparation, aerobic composting, vermicomposting, and anaerobic biogas digestion).

---

## 🌟 Master 20-Phase Implementation Matrix

| Phase | Title | Status | Key Deliverables |
|:---:|---|:---:|---|
| **01** | Project Environment Setup | **COMPLETED** | FastAPI directory scaffolding, health endpoints, Python 3.11 virtual environment. |
| **02** | Architecture & Database Design | **COMPLETED** | 24 SQLAlchemy models, Alembic migrations, database initialization seeds. |
| **03** | Professional UI/UX Design | **COMPLETED** | 27 responsive Material 3 Flutter screens, GoRouter routing, Riverpod state. |
| **04** | Vegetable Master Database | **COMPLETED** | 50 botanical vegetable records, taxonomy, search/filter CRUD endpoints. |
| **05** | Scientific Nutrient Database | **COMPLETED** | ICMR-NIN IFCT 2017 & USDA FDC verified biochemical fields and sources. |
| **06** | Image Collection & Dataset | **COMPLETED** | 360 stratified images (6 classes: carrot, potato, beetroot, cucumber, pumpkin, unsupported). |
| **07** | AI Model Development | **COMPLETED** | MobileNetV3 transfer learning pipeline, trained checkpoint (`smart_peel_mobilenetv3.pt`), 100% test accuracy. |
| **08** | AI Image Identification API | **COMPLETED** | `POST /scans/predict`, probabilistic ranking, uncertainty flag, negative sample rejection. |
| **09** | Flutter Camera & Upload | **COMPLETED** | Camera scan screen, gallery upload, AI prediction review and confirmation dialogs. |
| **10** | Core Nutrient Engine | **COMPLETED** | Dynamic biochemical profiles, proximate, vitamin, mineral, and antioxidant categorization. |
| **11** | Biological Explanations | **COMPLETED** | Health benefits, biological roles, and scientific citations in English & Tamil. |
| **12** | Weight Estimation Engine | **COMPLETED** | Empirical peel yield ratios, culinary cooking retention multipliers, DRI/RDA coverage. |
| **13** | Food Safety Engine | **COMPLETED** | Critical rules for potato solanine, cassava cyanogenic glucosides, taro oxalates, cucurbitacins. |
| **14** | Waste Valorization Engine | **COMPLETED** | 141 evidence-ranked valorization methods with hazardous material culinary inhibition. |
| **15** | Smart Waste Tracking | **COMPLETED** | Diversion logs, EPA WARM greenhouse gas calculations (0.52 kg CO2e/kg diverted). |
| **16** | User Authentication & History | **COMPLETED** | JWT bearer token security, profile management, password encryption, personal scan history. |
| **17** | Admin Dashboard & Audit Trail | **COMPLETED** | Executive overview metrics, chronological audit trail (`AdminAuditLog`), user governance. |
| **18** | Bilingual Localization | **COMPLETED** | English and Tamil (தமிழ்) UI strings, botanical nomenclature, translations dictionary API. |
| **19** | Reports & Scientific Validation | **COMPLETED** | ReportLab PDF report generation, full End-to-End integration test suite, unified test runner. |
| **20** | Deployment & Documentation | **COMPLETED** | Docker compose orchestration, multi-stage Dockerfiles, architectural and model card docs. |

---

## 🛠️ Technology Stack

- **Mobile & Web Frontend**: Flutter 3.47+, Dart 3.13+, Material 3 Design System, Riverpod 2.6+, GoRouter, Dio.
- **Backend API**: Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2.0, ReportLab 5.0+, Pytest 9.1+.
- **Artificial Intelligence**: PyTorch, MobileNetV3-Small, Torchvision, Pillow.
- **Database**: SQLite (local development), PostgreSQL (production-ready).
- **Containerization**: Docker, Docker Compose, Nginx Alpine.

---

## 🧪 Scientific Foundations

1. **ICMR - National Institute of Nutrition (NIN)**: *Indian Food Composition Tables (IFCT 2017)*, Hyderabad, India.
2. **USDA Agricultural Research Service**: *FoodData Central (FDC)*, Foundation Foods.
3. **EPA Waste Reduction Model (WARM)**: Organic waste diversion factor: $0.52 \text{ kg CO}_2\text{e}$ avoided per kg peel diverted from landfill.
4. **Food Safety Protocols**: Critical inhibition thresholds for solanine (> 200 mg/kg), cyanogenic glucosides, and calcium oxalate raphide crystals.

---

## 🚀 Quick Start Guide

### Option 1: Docker Compose (Production Setup)
```bash
docker compose up -d --build
```
- **Web App**: `http://localhost`
- **Backend API**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/api/v1/health/live`

### Option 2: Local Development Setup

#### Backend (FastAPI)
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend (Flutter)
```bash
cd frontend
flutter pub get
flutter run -d chrome
```

---

## 🔍 Validation & Testing

Run the unified system verification script:
```bash
python scripts/run_all_tests.py
```

### Verified Test Results:
- **Backend Pytest**: **105 passed**, 0 failed (across 13 test modules)
- **Frontend Flutter Tests**: **13 passed**, 0 failed
- **Flutter Analyzer**: **0 issues found** (clean static code analysis)
- **AI Model Checkpoint**: `smart_peel_mobilenetv3.pt` verified (100% test accuracy, 1.0 macro F1)
- **Database Integrity**: 24 tables, 50 botanical vegetables, 93 verified nutrient measurements

---

## 📖 System Documentation Links

- [System Architecture & Multi-Tier Design](file:///d:/Pattent%20project%2002/docs/SYSTEM_ARCHITECTURE.md)
- [AI Model Card (MobileNetV3)](file:///d:/Pattent%20project%2002/docs/AI_MODEL_CARD.md)
- [Scientific Methodology & Formulations](file:///d:/Pattent%20project%2002/docs/SCIENTIFIC_METHODOLOGY.md)
- [Production Deployment Guide](file:///d:/Pattent%20project%2002/docs/DEPLOYMENT_GUIDE.md)

---

## ⚖️ Scientific & Responsible Use Disclaimer
Smart Peel AI provides nutritional estimates based on verified scientific literature and empirical composition databases. It is intended for educational, domestic, and waste reduction valorization purposes. Visual identification is probabilistic and does not constitute certified analytical chemistry testing. Peels showing evidence of mould, extreme bitterness, or greening must not be consumed.
