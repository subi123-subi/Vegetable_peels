# SMART PEEL AI — PRODUCTION DEPLOYMENT GUIDE

## 1. Prerequisites
- Docker Engine 24.0+ and Docker Compose v2.20+
- (Optional bare-metal) Python 3.11+, Flutter 3.47+, SQLite 3.35+ or PostgreSQL 14+

---

## 2. Docker Compose Deployment (Recommended)

### Step 1: Clone and Configure Environment
```bash
git clone https://github.com/org/smart-peel-ai.git
cd smart-peel-ai
```

### Step 2: Build and Run Containers
```bash
docker compose up -d --build
```

### Step 3: Verify Container Health
```bash
docker compose ps
curl http://localhost:8000/api/v1/health/ready
```

---

## 3. Local Bare-Metal Setup

### Backend (FastAPI)
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend (Flutter Web)
```bash
cd frontend
flutter pub get
flutter run -d chrome
```

---

## 4. Environment Variables Configuration

| Variable | Default Value | Description |
|---|---|---|
| `APP_NAME` | `Smart Peel AI` | System title |
| `APP_ENV` | `production` | Environment (`development`, `production`) |
| `DATABASE_URL` | `sqlite:///./smart_peel_ai.db` | Connection string |
| `SECRET_KEY` | *(Set strong secret)* | JWT signature key |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Token lifetime (24 hours) |
| `PORT` | `8000` | Gateway listen port |
| `CORS_ORIGINS` | `["*"]` | Allowed CORS origins |

---

## 5. Automated Verification Runner
Run the unified 5-stage validation script anytime:
```bash
python scripts/run_all_tests.py
```
This automatically validates AI models, database seeds, all 105 backend pytest tests, Flutter analyzer, and all 13 Flutter widget tests.
