# app/models/member.py

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.models.base import Base


# Allowed values for membership_type — kept as plain strings (VARCHAR in DB),
# not a native MySQL ENUM, so new tiers (e.g. "senior", "honorary") can be
# added later without an ALTER TABLE migration. Validate against this list
# in your Pydantic schemas / service layer.
MEMBERSHIP_TYPES = ("single", "family", "student", "business")

# Same reasoning for gender — validate in the Pydantic layer if needed.
GENDERS = ("male", "female", "other")


class Member(Base):
    """Member table — from Aufnahme-Antrag (membership application form)."""
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)

    # Personal details
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    title = Column(String(50), nullable=True)          # Titel (optional)
    gender = Column(String(20), nullable=True)
    birth_date = Column(Date, nullable=True)

    # Membership details
    membership_type = Column(String(20), nullable=False)
    family_member_name = Column(String(200), nullable=True)  # only if membership_type == "family"

    # Address
    street = Column(String(200), nullable=False)
    postal_code = Column(String(20), nullable=False)
    city = Column(String(100), nullable=False)

    # Contact
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)

    # Signature
    signed_place = Column(String(100), nullable=True)
    signed_date = Column(Date, nullable=True)

    # Relationships
    bank_account = relationship("BankAccount", back_populates="member", uselist=False, cascade="all, delete-orphan")
    consent = relationship("Consent", back_populates="member", uselist=False, cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="member", cascade="all, delete-orphan")