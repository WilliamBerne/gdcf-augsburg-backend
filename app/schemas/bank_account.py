# app/schemas/bank_account.py

from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, model_validator


class BankAccountBase(BaseModel):
    account_holder_name: str
    street: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    bank_name: Optional[str] = None
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

    @model_validator(mode="after")
    def reject_null_required_fields(self):
        required_fields = {"account_holder_name", "iban"}
        null_fields = sorted(
            field
            for field in required_fields & self.model_fields_set
            if getattr(self, field) is None
        )
        if null_fields:
            raise ValueError(
                f"Fields cannot be null: {', '.join(null_fields)}"
            )
        return self


class BankAccountRead(BankAccountBase):
    id: int
    member_id: int
    model_config = ConfigDict(from_attributes=True)