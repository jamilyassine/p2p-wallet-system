from app.db.session import Base
from datetime import datetime

from sqlalchemy import Integer, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    balance: Mapped[float] = mapped_column(
        Numeric,
        default=0
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )





