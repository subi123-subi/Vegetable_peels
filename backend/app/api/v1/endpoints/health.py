from datetime import datetime, timezone
import os
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/health", summary="Health Check")
async def health_check():
    """
    Returns system health status, version, environment details, and component status.
    """
    db_available = True
    storage_dir = settings.UPLOAD_DIR
    storage_writable = False

    try:
        os.makedirs(storage_dir, exist_ok=True)
        test_file = os.path.join(storage_dir, ".test_write")
        with open(test_file, "w") as f:
            f.write("ok")
        if os.path.exists(test_file):
            os.remove(test_file)
            storage_writable = True
    except Exception:
        storage_writable = False

    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "api": "ok",
            "storage": "writable" if storage_writable else "error",
            "database_configured": bool(settings.DATABASE_URL),
        },
    }
