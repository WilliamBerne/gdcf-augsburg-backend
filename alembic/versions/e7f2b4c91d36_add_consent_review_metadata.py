"""add consent form review and withdrawal metadata

Revision ID: e7f2b4c91d36
Revises: c3a1e8f70b42
Create Date: 2026-07-23

"""

from alembic import op
import sqlalchemy as sa


revision = "e7f2b4c91d36"
down_revision = "c3a1e8f70b42"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "consents",
        sa.Column(
            "form_version",
            sa.String(length=100),
            nullable=False,
            server_default="gdcf-consent-de-zh-v1",
        ),
    )
    op.add_column("consents", sa.Column("signed_document_id", sa.Integer(), nullable=True))
    op.add_column("consents", sa.Column("data_protection_signer_role", sa.String(length=20), nullable=True))
    op.add_column(
        "consents",
        sa.Column(
            "data_protection_signature_status",
            sa.String(length=20),
            nullable=False,
            server_default="pending_review",
        ),
    )
    op.add_column("consents", sa.Column("data_protection_reviewed_by", sa.String(length=200), nullable=True))
    op.add_column("consents", sa.Column("data_protection_reviewed_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("consents", sa.Column("data_protection_withdrawn_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("consents", sa.Column("newsletter_withdrawn_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("consents", sa.Column("photo_video_signer_role", sa.String(length=20), nullable=True))
    op.add_column(
        "consents",
        sa.Column(
            "photo_video_signature_status",
            sa.String(length=20),
            nullable=False,
            server_default="pending_review",
        ),
    )
    op.add_column("consents", sa.Column("photo_video_reviewed_by", sa.String(length=200), nullable=True))
    op.add_column("consents", sa.Column("photo_video_reviewed_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("consents", sa.Column("photo_video_withdrawn_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("consents", sa.Column("photo_video_minor_co_signed", sa.Boolean(), nullable=True))
    op.add_column(
        "consents",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.add_column(
        "consents",
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
    )
    op.create_foreign_key(
        "fk_consents_signed_document_id_documents",
        "consents",
        "documents",
        ["signed_document_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_consents_signed_document_id_documents",
        "consents",
        type_="foreignkey",
    )
    for column_name in (
        "updated_at",
        "created_at",
        "photo_video_minor_co_signed",
        "photo_video_withdrawn_at",
        "photo_video_reviewed_at",
        "photo_video_reviewed_by",
        "photo_video_signature_status",
        "photo_video_signer_role",
        "newsletter_withdrawn_at",
        "data_protection_withdrawn_at",
        "data_protection_reviewed_at",
        "data_protection_reviewed_by",
        "data_protection_signature_status",
        "data_protection_signer_role",
        "signed_document_id",
        "form_version",
    ):
        op.drop_column("consents", column_name)
