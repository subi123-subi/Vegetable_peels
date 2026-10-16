# SMART PEEL AI
## Intelligent Vegetable Peel Nutrient Identification and Food Waste Valorization System

Smart Peel AI is an end-to-end, scientifically responsible software application designed to identify vegetable peels from photographs, provide referenced biochemical and nutritional composition data, calculate weight-based nutrient intake estimates, enforce strict food safety rules, and recommend evidence-based valorization strategies (such as composting, biogas feedstock, bio-based materials, and safe culinary preparation).

---

## 🌟 Core Pillars

1. **Computer Vision & Classification**: MobileNetV3 transfer learning pipeline trained on vegetable peel photography, featuring confidence thresholds and unsupported sample rejection.
2. **Scientific Nutrient Engine**: Traceable nutrient profiles derived from verified standards (ICMR-NIN Indian Food Composition Tables, USDA FoodData Central, peer-reviewed literature). Whole-vegetable data is never conflated with peel data.
3. **Food Safety Engine**: Enforces strict biological and chemical safety rules (e.g., green potato glycoalkaloid hazards, cassava cyanogenic glucosides, bitter gourd cucurbitacins, pesticide warnings).
4. **Valorization & Waste Diversion Tracking**: Practical, evidence-based recommendations for households, restaurants, farmers, and industries with verifiable waste-diverted tracking.
5. **Bilingual Accessibility**: Full English and Tamil (தமிழ்) interface, localization, and nomenclature.

---

## 🛠️ Technology Stack

- **Frontend**: Flutter 3.47+, Dart 3.13+, Material 3, Riverpod state management, GoRouter, Dio.
- **Backend**: Python 3.11, FastAPI, Pydantic v2, SQLAlchemy, Alembic, JWT Authentication, Pytest.
- **AI & ML**: MobileNetV3, TensorFlow/Keras, OpenCV / Pillow, NumPy, Scikit-learn.
- **Database**: SQLite (local development), PostgreSQL (production-ready).
- **Reports**: PDF Generation (ReportLab), CSV data export.

---

## 📁 Project Directory Structure

```
Pattent project 02/
├── ai/                      # AI training pipeline, datasets & exported weights
│   ├── datasets/
│   │   ├── raw/             # Raw classified image sets
│   │   └── processed/       # Preprocessed and augmented data splits
│   ├── models/              # Exported Keras/TFLite models and labels
│   ├── notebooks/           # Exploratory data analysis & model development
│   └── scripts/             # Automated training and evaluation scripts
├── backend/                 # FastAPI backend server
│   ├── app/
│   │   ├── api/v1/          # Versioned API routes (health, scans, nutrients, admin)
│   │   ├── core/            # App configuration, security & logging
│   │   ├── db/              # SQLAlchemy session, engine & base models
│   │   ├── models/          # ORM database models
│   │   └── schemas/         # Pydantic validation schemas
│   ├── tests/               # Pytest automated test suites
│   ├── requirements.txt     # Python backend dependencies
│   ├── .env.example         # Environment template
│   └── .env                 # Local environment configuration
├── frontend/                # Flutter application
│   ├── lib/                 # App source code (Material 3 UI, Riverpod state)
│   ├── test/                # Flutter unit & widget tests
│   └── pubspec.yaml         # Dart dependencies
├── docs/                    # System documentation & research archives
│   ├── architecture/        # System diagrams & database schemas
│   ├── research/            # Scientific nutrient references & papers
│   └── api/                 # OpenAPI specs & integration guides
├── .gitignore               # Multi-stack git ignore rules
├── pytest.ini               # Pytest discovery configuration
└── README.md                # System documentation
```

---

## 🚀 Getting Started

### Backend Setup
1. Open PowerShell and navigate to the backend folder:
   ```powershell
   cd backend
   ```
2. Activate the virtual environment:
   ```powershell
   .venv\Scripts\activate
   ```
3. Run the development server:
   ```powershell
   python -m uvicorn app.main:app --reload --port 8000
   ```
4. Access the API documentation at `http://127.0.0.1:8000/api/v1/docs`.

### Frontend Setup
1. In a separate terminal, navigate to `frontend`:
   ```powershell
   cd frontend
   ```
2. Run Flutter app:
   ```powershell
   flutter run -d chrome    # Or windows / android
   ```
