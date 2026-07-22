# app/schemas/bank_account.py

from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class BankAccountBase(BaseModel):
    account_holder_name: str
    street: str
    postal_code: str
    city: str
    bank_name: str
    iban: str
    mandate_place: Optional[str] = None
    mandate_date: Optional[date] = None


class BankAccountCreate(BankAccountBase):
    member_id: int


class BankAccountUpdate(BaseModel):
    account_holder_name: Optional[str] = None
    street: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    bank_name: Optional[str] = None
    iban: Optional[str] = None
    mandate_place: Optional[str] = None
    mandate_date: Optional[date] = None


class BankAccountRead(BankAccountBase):
    id: int
    member_id: int
    model_config = ConfigDict(from_attributes=True)