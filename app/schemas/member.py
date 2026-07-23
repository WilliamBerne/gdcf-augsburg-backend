# app/schemas/member.py

from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, ConfigDict, model_validator

MembershipType = Literal["single", "family", "student", "business"]
Gender = Literal["male", "female", "other"]


class MemberBase(BaseModel):
    last_name: str
    first_name: str
    title: Optional[str] = None
    gender: Optional[Gender] = None
    birth_date: Optional[date] = None
    membership_type: MembershipType
    family_member_name: Optional[str] = None
    street: str
    postal_code: str
    city: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    signed_place: Optional[str] = None
    signed_date: Optional[date] = None


class MemberCreate(MemberBase):
    """Fields required to create a new member."""
    pass


class MemberUpdate(BaseModel):
    """All fields optional — only send what you want to change."""
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    title: Optional[str] = None
    gender: Optional[Gender] = None
    birth_date: Optional[date] = None
    membership_type: Optional[MembershipType] = None
    family_member_name: Optional[str] = None
    street: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    signed_place: Optional[str] = None
    signed_date: Optional[date] = None

    @model_validator(mode="after")
    def reject_null_required_fields(self):
        required_fields = {
            "last_name",
            "first_name",
            "membership_type",
            "street",
            "postal_code",
            "city",
        }
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


class MemberRead(MemberBase):
    """What gets returned to API clients."""
    id: int
    model_config = ConfigDict(from_attributes=True)  # allows reading from SQLAlchemy objects