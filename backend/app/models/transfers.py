from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import (
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class TransferStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Transfer(Base):
    __tablename__ = "transfers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    request_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )

    sender_wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets.id"),
        nullable=False,
    )

    receiver_wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets.id"),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    status: Mapped[TransferStatus] = mapped_column(
        SqlEnum(TransferStatus),
        default=TransferStatus.PENDING,
        nullable=False,
    )

    error_code: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    response_json: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    sender_wallet: Mapped["Wallet"] = relationship(
        foreign_keys=[sender_wallet_id],
        back_populates="sent_transfers",
    )

    receiver_wallet: Mapped["Wallet"] = relationship(
        foreign_keys=[receiver_wallet_id],
        back_populates="received_transfers",
    )

    ledger_entries: Mapped[list["LedgerEntry"]] = relationship(
        back_populates="transfer",
    )




if TYPE_CHECKING:
    from app.models.wallet import Wallet
    from app.models.ledger_entry import LedgerEntry