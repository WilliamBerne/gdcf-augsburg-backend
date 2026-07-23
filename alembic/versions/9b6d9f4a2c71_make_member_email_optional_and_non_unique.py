"""make member email optional and non-unique

Revision ID: 9b6d9f4a2c71
Revises: 5fd753c458ee
Create Date: 2026-07-23

"""

from alembic import op
import sqlalchemy as sa


revision = "9b6d9f4a2c71"
down_revision = "5fd753c458ee"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("email", "members", type_="unique")
    op.alter_column(
        "members",
        "email",
        existing_type=sa.String(length=255),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "members",
        "email",
        existing_type=sa.String(length=255),
        nullable=False,
    )
    op.create_unique_constraint("email", "members", ["email"])
