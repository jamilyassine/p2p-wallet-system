from datetime import datetime, UTC
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.ledger_account import LedgerAccount
from app.models.funding import Funding


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
            "ledger_account_id",
            "entry_type",
            name="uq_transfer_ledger_account_entry_type",
        ),
        CheckConstraint(
            "(transfer_id IS NOT NULL) <> (funding_id IS NOT NULL)",
            name="ck_ledger_entry_transfer_or_funding",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    transfer_id: Mapped[int | None] = mapped_column(
        ForeignKey("transfers.id"),
        nullable=True,
    )

    ledger_account_id: Mapped[int] = mapped_column(
        ForeignKey("ledger_accounts.id"),
        nullable=False,
    )

    funding_id: Mapped[int | None] = mapped_column(
        ForeignKey("fundings.id"),
        nullable=True,
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

    ledger_account: Mapped["LedgerAccount"] = relationship(
        back_populates="ledger_entries",
    )

    funding: Mapped["Funding"] = relationship(
        back_populates="ledger_entries",
    )


if TYPE_CHECKING:
    from app.models.transfers import Transfer
    
