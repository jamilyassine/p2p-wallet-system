from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class WalletCreate(BaseModel):
    user_id: int


class WalletResponse(BaseModel):
    id: int
    user_id: int
    balance: Decimal
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )