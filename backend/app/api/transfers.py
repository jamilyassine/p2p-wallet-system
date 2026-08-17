from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.transfer import (
    TransferRequest,
    TransferResponse,
    PaginatedTransfersResponse,
)
from app.services import transfer_service


router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"],
)


@router.post(
    "/",
    response_model=TransferResponse,
)
def create_transfer_endpoint(
    request: TransferRequest,
    db: Session = Depends(get_db),
):
    response = transfer_service.transfer_money(
        db=db,
        request_id=request.request_id,
        sender_id=request.sender_id,
        receiver_id=request.receiver_id,
        amount=request.amount,
    )

    if response["status"] == "FAILED":
        return JSONResponse(
            status_code=400,
            content=response,
        )

    return response


@router.get(
    "/user/{user_id}",
    response_model=PaginatedTransfersResponse,
)
def get_transfers_by_user_id_endpoint(
    user_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return transfer_service.get_transfers_by_user_id(
        db,
        user_id,
        page,
        limit,
    )

