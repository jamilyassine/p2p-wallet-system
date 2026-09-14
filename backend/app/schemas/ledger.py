from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.ledger_entry import LedgerEntryType


class LedgerEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    transfer_id: int
    wallet_id: int
    wallet_user_name: str
    entry_type: LedgerEntryType
    amount: Decimal
    created_at: datetime

class PaginatedLedgerResponse(BaseModel):
    transactions: list[LedgerEntryResponse]
    total: int
    current_page: int
    page_size: int