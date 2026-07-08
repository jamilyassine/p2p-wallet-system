from pydantic import BaseModel
from decimal import Decimal

class TransferRequest(BaseModel):
    sender_id: int
    receiver_id: int
    amount: Decimal