"""add member archival state

Revision ID: a6d3e9f2184b
Revises: f4a8c2d71e05
Create Date: 2026-07-23

"""

from alembic import op
import sqlalchemy as sa


revision = "a6d3e9f2184b"
down_revision = "f4a8c2d71e05"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "members",
        sa.Column(
            "membership_status",
            sa.String(length=20),
            nullable=False,
            server_default="active",
        ),
    )
    op.add_column(
        "members",
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_members_membership_status",
        "members",
        ["membership_status"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_members_membership_status", table_name="members")
    op.drop_column("members", "archived_at")
    op.drop_column("members", "membership_status")
