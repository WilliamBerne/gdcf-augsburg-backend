# app/schemas/consent.py

from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ConsentBase(BaseModel):
    data_protection_consent: bool = False
    data_protection_signed_name: Optional[str] = None
    data_protection_signed_place: Optional[str] = None
    data_protection_signed_date: Optional[date] = None

    newsletter_opt_in: bool = False

    photo_video_consent: bool = False
    photo_video_signed_name: Optional[str] = None
    photo_video_signed_place: Optional[str] = None
    photo_video_signed_date: Optional[date] = None

    guardian_signed_name: Optional[str] = None
    minor_signed_name: Optional[str] = None


class ConsentCreate(ConsentBase):
    member_id: int


class ConsentUpdate(BaseModel):
    data_protection_consent: Optional[bool] = None
    newsletter_opt_in: Optional[bool] = None
    photo_video_consent: Optional[bool] = None
    guardian_signed_name: Optional[str] = None
    minor_signed_name: Optional[str] = None


class ConsentRead(ConsentBase):
    id: int
    member_id: int
    model_config = ConfigDict(from_attributes=True)