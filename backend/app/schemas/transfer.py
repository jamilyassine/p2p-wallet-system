from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class TransferRequest(BaseModel):
    sender_id: int
    receiver_id: int
    amount: Decimal


class TransferResponse(BaseModel):
    sender_balance: Decimal
    receiver_balance: Decimal


class TransferRead(BaseModel):
    id: int
    sender_wallet_id: int
    receiver_wallet_id: int
    amount: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
