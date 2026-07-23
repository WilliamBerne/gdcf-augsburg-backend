"""make nonessential bank account details optional

Revision ID: c3a1e8f70b42
Revises: 9b6d9f4a2c71
Create Date: 2026-07-23

"""

from alembic import op
import sqlalchemy as sa


revision = "c3a1e8f70b42"
down_revision = "9b6d9f4a2c71"
branch_labels = None
depends_on = None


def upgrade() -> None:
    for column_name, column_type in (
        ("street", sa.String(length=200)),
        ("postal_code", sa.String(length=20)),
        ("city", sa.String(length=100)),
        ("bank_name", sa.String(length=200)),
    ):
        op.alter_column(
            "bank_accounts",
            column_name,
            existing_type=column_type,
            nullable=True,
        )


def downgrade() -> None:
    for column_name, column_type in (
        ("street", sa.String(length=200)),
        ("postal_code", sa.String(length=20)),
        ("city", sa.String(length=100)),
        ("bank_name", sa.String(length=200)),
    ):
        op.alter_column(
            "bank_accounts",
            column_name,
            existing_type=column_type,
            nullable=False,
        )
