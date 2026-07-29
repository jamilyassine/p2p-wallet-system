from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Wallet(Base):
    __tablename__ = "wallets"

    __table_args__ = (
        CheckConstraint(
            "balance >= 0",
            name="check_wallet_balance_non_negative",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="wallet",
    )

    sent_transfers: Mapped[list["Transfer"]] = relationship(
        foreign_keys="Transfer.sender_wallet_id",
        back_populates="sender_wallet",
    )

    received_transfers: Mapped[list["Transfer"]] = relationship(
        foreign_keys="Transfer.receiver_wallet_id",
        back_populates="receiver_wallet",
    )

    ledger_entries: Mapped[list["LedgerEntry"]] = relationship(
        back_populates="wallet",
    )




if TYPE_CHECKING:
    from app.models.transfers import Transfer
    from app.models.user import User
    from app.models.ledger_entry import LedgerEntry

    