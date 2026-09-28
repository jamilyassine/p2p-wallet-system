"""add ledger accounts

Revision ID: 6381d0c1d1fe
Revises: f3303822ed47
Create Date: 2026-09-23 21:13:18.291694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6381d0c1d1fe"
down_revision: Union[str, Sequence[str], None] = "f3303822ed47"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create ledger_accounts
    op.create_table(
        "ledger_accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "account_type",
            sa.Enum(
                "USER_WALLET",
                "SYSTEM",
                name="ledgeraccounttype",
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # 2. Create one USER_WALLET ledger account for every existing wallet
    op.execute(
        """
        INSERT INTO ledger_accounts (account_type)
        SELECT 'USER_WALLET'
        FROM wallets
        """
    )

    # 3. Add wallet.ledger_account_id as nullable temporarily
    op.add_column(
        "wallets",
        sa.Column(
            "ledger_account_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # 4. Match each existing wallet with one newly-created ledger account
    op.execute(
        """
        WITH numbered_wallets AS (
            SELECT
                id,
                ROW_NUMBER() OVER (ORDER BY id) AS rn
            FROM wallets
        ),
        numbered_accounts AS (
            SELECT
                id,
                ROW_NUMBER() OVER (ORDER BY id) AS rn
            FROM ledger_accounts
        )
        UPDATE wallets w
        SET ledger_account_id = a.id
        FROM numbered_wallets nw
        JOIN numbered_accounts a
            ON nw.rn = a.rn
        WHERE w.id = nw.id
        """
    )

    # 5. Add wallet constraints
    op.alter_column(
        "wallets",
        "ledger_account_id",
        nullable=False,
    )

    op.create_unique_constraint(
        "uq_wallets_ledger_account_id",
        "wallets",
        ["ledger_account_id"],
    )

    op.create_foreign_key(
        "fk_wallets_ledger_account_id",
        "wallets",
        "ledger_accounts",
        ["ledger_account_id"],
        ["id"],
    )

    # 6. Add ledger_entries.ledger_account_id temporarily nullable
    op.add_column(
        "ledger_entries",
        sa.Column(
            "ledger_account_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # 7. Backfill ledger account from the existing wallet_id
    op.execute(
        """
        UPDATE ledger_entries le
        SET ledger_account_id = w.ledger_account_id
        FROM wallets w
        WHERE le.wallet_id = w.id
        """
    )

    # 8. Replace old transfer uniqueness constraint
    op.drop_constraint(
        "uq_transfer_wallet_entry_type",
        "ledger_entries",
        type_="unique",
    )

    op.create_unique_constraint(
        "uq_transfer_ledger_account_entry_type",
        "ledger_entries",
        [
            "transfer_id",
            "ledger_account_id",
            "entry_type",
        ],
    )

    # 9. Replace wallet FK with ledger account FK
    op.drop_constraint(
        "ledger_entries_wallet_id_fkey",
        "ledger_entries",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "fk_ledger_entries_ledger_account_id",
        "ledger_entries",
        "ledger_accounts",
        ["ledger_account_id"],
        ["id"],
    )

    # 10. ledger_account_id is now mandatory
    op.alter_column(
        "ledger_entries",
        "ledger_account_id",
        nullable=False,
    )

    # 11. Remove old wallet_id
    op.drop_column(
        "ledger_entries",
        "wallet_id",
    )


def downgrade() -> None:
    # Restore wallet_id on ledger_entries
    op.add_column(
        "ledger_entries",
        sa.Column(
            "wallet_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    # Recover wallet_id from ledger_account -> wallet
    op.execute(
        """
        UPDATE ledger_entries le
        SET wallet_id = w.id
        FROM wallets w
        WHERE le.ledger_account_id = w.ledger_account_id
        """
    )

    op.alter_column(
        "ledger_entries",
        "wallet_id",
        nullable=False,
    )

    op.create_foreign_key(
        "ledger_entries_wallet_id_fkey",
        "ledger_entries",
        "wallets",
        ["wallet_id"],
        ["id"],
    )

    op.drop_constraint(
        "fk_ledger_entries_ledger_account_id",
        "ledger_entries",
        type_="foreignkey",
    )

    op.drop_constraint(
        "uq_transfer_ledger_account_entry_type",
        "ledger_entries",
        type_="unique",
    )

    op.create_unique_constraint(
        "uq_transfer_wallet_entry_type",
        "ledger_entries",
        [
            "transfer_id",
            "wallet_id",
            "entry_type",
        ],
    )

    op.drop_column(
        "ledger_entries",
        "ledger_account_id",
    )

    op.drop_constraint(
        "fk_wallets_ledger_account_id",
        "wallets",
        type_="foreignkey",
    )

    op.drop_constraint(
        "uq_wallets_ledger_account_id",
        "wallets",
        type_="unique",
    )

    op.drop_column(
        "wallets",
        "ledger_account_id",
    )

    op.drop_table("ledger_accounts")