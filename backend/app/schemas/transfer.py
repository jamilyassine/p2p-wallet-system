from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TransferRequest(BaseModel):
    request_id: UUID
    sender_id: int
    receiver_id: int
    amount: Decimal


class TransferResponse(BaseModel):
    status: str
    transfer_id: int | None = None
    amount: Decimal | None = None
    sender_id: int | None = None
    receiver_id: int | None = None
    error_code: str | None = None


class TransferRead(BaseModel):
    id: int
    sender_wallet_id: int
    receiver_wallet_id: int
    sender_name: str
    receiver_name: str
    amount: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

class PaginatedTransfersResponse(BaseModel):
    current_page: int
    page_size: int
    total: int
    transactions: list[TransferRead]