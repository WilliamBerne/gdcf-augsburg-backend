"""remove legacy consent signature name columns

Revision ID: f4a8c2d71e05
Revises: e7f2b4c91d36
Create Date: 2026-07-23

"""

from alembic import op
import sqlalchemy as sa


revision = "f4a8c2d71e05"
down_revision = "e7f2b4c91d36"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("consents", "minor_signed_name")
    op.drop_column("consents", "guardian_signed_name")


def downgrade() -> None:
    op.add_column(
        "consents",
        sa.Column("guardian_signed_name", sa.String(length=200), nullable=True),
    )
    op.add_column(
        "consents",
        sa.Column("minor_signed_name", sa.String(length=200), nullable=True),
    )
