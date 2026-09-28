from datetime import datetime, UTC
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Funding(Base):
    __tablename__ = "fundings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    funding_id: Mapped[UUID] = mapped_column(
        default=uuid4,
        unique=True,
        nullable=False,
    )

    wallet_id: Mapped[int] = mapped_column(
        ForeignKey("wallets.id"),
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

    wallet: Mapped["Wallet"] = relationship(
        back_populates="fundings",
    )

    ledger_entries: Mapped[list["LedgerEntry"]] = relationship(
        back_populates="funding",
    )


if TYPE_CHECKING:
    from app.models.wallet import Wallet
    from app.models.ledger_entry import LedgerEntry