from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.funding_service import fund_wallet
from app.core.dependencies import get_funding_db, require_admin

router = APIRouter(
    prefix="/admin/funding",
    tags=["Admin Funding"],
)


@router.post("")
def create_funding(
    email: str,
    amount: Decimal,
    db: Session = Depends(get_funding_db),
    admin: User = Depends(require_admin),
):
    return fund_wallet(
        db=db,
        email=email,
        amount=amount,
    )
