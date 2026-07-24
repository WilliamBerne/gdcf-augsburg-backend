"""use external identity for users

Revision ID: d9c4a7e2156f
Revises: b8e5f1a73c29
Create Date: 2026-07-24

"""

from alembic import op
import sqlalchemy as sa


revision = "d9c4a7e2156f"
down_revision = "b8e5f1a73c29"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "auth_provider",
            sa.String(length=50),
            nullable=False,
            server_default="wordpress",
        ),
    )
    op.add_column(
        "users",
        sa.Column("external_subject", sa.String(length=255), nullable=False),
    )
    op.create_unique_constraint(
        "uq_users_auth_provider_external_subject",
        "users",
        ["auth_provider", "external_subject"],
    )
    op.drop_column("users", "password_hash")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=False,
            server_default="",
        ),
    )
    op.alter_column(
        "users",
        "password_hash",
        existing_type=sa.String(length=255),
        existing_nullable=False,
        server_default=None,
    )
    op.drop_constraint(
        "uq_users_auth_provider_external_subject",
        "users",
        type_="unique",
    )
    op.drop_column("users", "external_subject")
    op.drop_column("users", "auth_provider")
