from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


MembershipRole = Literal["member", "membership_staff", "membership_admin"]


class UserCreate(BaseModel):
    email: EmailStr
    auth_provider: str = Field(default="wordpress", min_length=1, max_length=50)
    external_subject: str = Field(min_length=1, max_length=255)
    role: MembershipRole = "member"
    member_id: Optional[int] = None


class UserUpdate(BaseModel):
    role: Optional[MembershipRole] = None
    is_active: Optional[bool] = None
    member_id: Optional[int] = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    auth_provider: str
    external_subject: str
    role: MembershipRole
    is_active: bool
    member_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
