from fastapi import APIRouter, status, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.db.session import get_db

router = APIRouter()

@router.get("/health")
def health(db: Session = Depends(get_db)):

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







