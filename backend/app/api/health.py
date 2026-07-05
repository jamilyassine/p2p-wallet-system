from fastapi import APIRouter, status
from app.db.session import SessionLocal
from sqlalchemy import text
from fastapi.responses import JSONResponse


router = APIRouter()

@router.get("/health")
def health():
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "application": "running",
            "database": "connected"
        }

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "application": "running",
                "database": "disconnected"
            }
        )

    finally:
        db.close()






