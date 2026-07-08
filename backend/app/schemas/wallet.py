from pydantic import BaseModel
from datetime import datetime


class WalletCreate(BaseModel):
    user_id: int


class WalletResponse(BaseModel):
    id: int
    user_id: int
    balance: float
    created_at: datetime

