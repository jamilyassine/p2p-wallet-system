"""enforce single system ledger account

Revision ID: 2cefaaa1c516
Revises: 6381d0c1d1fe
Create Date: 2026-09-23 22:22:28.440626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cefaaa1c516'
down_revision: Union[str, Sequence[str], None] = '6381d0c1d1fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "uq_single_system_ledger_account",
        "ledger_accounts",
        ["account_type"],
        unique=True,
        postgresql_where=sa.text("account_type = 'SYSTEM'"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_single_system_ledger_account",
        table_name="ledger_accounts",
    )