# app/schemas/member.py

from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, ConfigDict

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


class MemberRead(MemberBase):
    """What gets returned to API clients."""
    id: int
    model_config = ConfigDict(from_attributes=True)  # allows reading from SQLAlchemy objects