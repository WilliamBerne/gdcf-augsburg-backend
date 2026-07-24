from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


MEMBERSHIP_ROLES = ("member", "membership_staff", "membership_admin")


class User(Base):
    """External identity mapped to membership-application authorization."""

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint(
            "auth_provider",
            "external_subject",
            name="uq_users_auth_provider_external_subject",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    auth_provider = Column(String(50), nullable=False, default="wordpress")
    external_subject = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="member", index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    member_id = Column(
        Integer,
        ForeignKey("members.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    member = relationship("Member", back_populates="user")
