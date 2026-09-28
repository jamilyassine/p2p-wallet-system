from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.funding_service import fund_wallet


router = APIRouter(
    prefix="/funding",
    tags=["Funding"],
)


@router.post("")
def create_funding(
    email: str,
    amount: Decimal,
    db: Session = Depends(get_db),
):
    return fund_wallet(
        db=db,
        email=email,
        amount=amount,
    )