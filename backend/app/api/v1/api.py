from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    vegetables,
    nutrients,
    scans,
    safety,
    reuse,
    waste_tracking,
    auth,
    admin,
    translations,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["User Authentication & Profile"])
api_router.include_router(vegetables.router, prefix="/vegetables", tags=["Vegetables Catalogue"])
api_router.include_router(nutrients.router, prefix="/nutrients", tags=["Nutrient Datasets"])
api_router.include_router(scans.router, prefix="/scans", tags=["AI Scan & Image Identification"])
api_router.include_router(safety.router, prefix="/safety", tags=["Food Safety Engine"])
api_router.include_router(reuse.router, prefix="/reuse", tags=["Waste Utilization Engine"])
api_router.include_router(waste_tracking.router, prefix="/waste-tracking", tags=["Smart Waste Tracking & Diversion"])
api_router.include_router(admin.router, prefix="/admin", tags=["Administrator Console & Audit"])
api_router.include_router(translations.router, prefix="/translations", tags=["Bilingual Localization & Dictionary"])
