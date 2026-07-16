# app/models/member.py

from sqlalchemy import Column, Integer, String, Date
from app.models.base import Base

class Member(Base):
    """Member table."""
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50), nullable=True)
    birth_date = Column(Date, nullable=True)