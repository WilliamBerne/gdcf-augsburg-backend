# app/models/bank_account.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class BankAccount(Base):
    """SEPA direct-debit mandate details, one per member."""
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False, unique=True)

    account_holder_name = Column(String(200), nullable=False)  # Kontoinhaber
    street = Column(String(200), nullable=True)
    postal_code = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    bank_name = Column(String(200), nullable=True)             # Kreditinstitut
    iban = Column(String(34), nullable=False)                  # IBAN, max 34 chars per ISO 13616

    mandate_place = Column(String(100), nullable=True)         # Ort
    mandate_date = Column(Date, nullable=True)                 # Datum

    member = relationship("Member", back_populates="bank_account")