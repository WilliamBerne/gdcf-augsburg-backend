# app/api/routers/member.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate, MemberRead

router = APIRouter(prefix="/members", tags=["members"])


@router.post("/", response_model=MemberRead, status_code=201)
def create_member(payload: MemberCreate, db: Session = Depends(get_db)):
    existing = db.query(Member).filter(Member.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="A member with this email already exists")

    member = Member(**payload.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@router.get("/", response_model=list[MemberRead])
def list_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Member).offset(skip).limit(limit).all()


@router.get("/{member_id}", response_model=MemberRead)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.patch("/{member_id}", response_model=MemberRead)
def update_member(member_id: int, payload: MemberUpdate, db: Session = Depends(get_db)):
    member = db.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(member, field, value)

    db.commit()
    db.refresh(member)
    return member


@router.delete("/{member_id}", status_code=204)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.commit()