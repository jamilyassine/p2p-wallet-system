from app.db.session import Base
from datetime import datetime
from app.models.transfers import Transfer

from sqlalchemy import Integer, Numeric, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


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
        primary_key=True
    )

    balance: Mapped[float] = mapped_column(
        Numeric,
        default=0
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user: Mapped["User"] = relationship(
        back_populates="wallet"
    )

    sent_transfers: Mapped[list["Transfer"]] = relationship(
        foreign_keys=[Transfer.sender_wallet_id],
        back_populates="sender_wallet",
    )

    received_transfers: Mapped[list["Transfer"]] = relationship(
        foreign_keys=[Transfer.receiver_wallet_id],
        back_populates="receiver_wallet",
    )





