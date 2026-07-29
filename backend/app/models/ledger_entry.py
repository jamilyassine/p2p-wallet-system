from datetime import datetime,UTC
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, UniqueConstraint

from sqlalchemy import (
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    Numeric,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.session import Base

class LedgerEntryType(str, Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"
    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_ledger_amount_positive",
        ),
        UniqueConstraint(
            "transfer_id",
            "wallet_id",
            "entry_type",
            name="uq_transfer_wallet_entry_type",
        ),
    )


    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    transfer_id: Mapped[int] = mapped_column(
        ForeignKey("transfers.id"),
        nullable=False,
    )

    wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets.id"),
        nullable=False,
    )

    entry_type: Mapped[LedgerEntryType] = mapped_column(
        SqlEnum(LedgerEntryType),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    transfer: Mapped["Transfer"] = relationship(
        back_populates="ledger_entries",
    )

    wallet: Mapped["Wallet"] = relationship(
        back_populates="ledger_entries",
    )


if TYPE_CHECKING:
    from app.models.transfers import Transfer
    from app.models.wallet import Wallet

    
