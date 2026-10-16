from fastapi import APIRouter
from app.api.v1.endpoints import health, vegetables, nutrients

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(vegetables.router, prefix="/vegetables", tags=["Vegetables Catalogue"])
api_router.include_router(nutrients.router, prefix="/nutrients", tags=["Nutrient Datasets"])
