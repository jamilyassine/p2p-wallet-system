from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SqlEnum, Index, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class LedgerAccountType(str, Enum):
    USER_WALLET = "USER_WALLET"
    SYSTEM = "SYSTEM"


class LedgerAccount(Base):
    __tablename__ = "ledger_accounts"

    __table_args__ = (
        Index(
            "uq_single_system_ledger_account",
            "account_type",
            unique=True,
            postgresql_where=text("account_type = 'SYSTEM'"),
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    account_type: Mapped[LedgerAccountType] = mapped_column(
        SqlEnum(LedgerAccountType),
        nullable=False,
    )

    wallet: Mapped["Wallet"] = relationship(
        back_populates="ledger_account",
        uselist=False,
    )

    ledger_entries: Mapped[list["LedgerEntry"]] = relationship(
        back_populates="ledger_account",
    )


if TYPE_CHECKING:
    from app.models.ledger_entry import LedgerEntry
    from app.models.wallet import Wallet





