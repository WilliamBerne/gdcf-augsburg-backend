# app/api/routers/bank_account.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.member import Member
from app.models.bank_account import BankAccount
from app.schemas.bank_account import BankAccountCreate, BankAccountUpdate, BankAccountRead

router = APIRouter(prefix="/bank-accounts", tags=["bank-accounts"])


@router.post("/", response_model=BankAccountRead, status_code=201)
def create_bank_account(payload: BankAccountCreate, db: Session = Depends(get_db)):
    member = db.get(Member, payload.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    existing = db.query(BankAccount).filter(BankAccount.member_id == payload.member_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="This member already has a bank account on file")

    account = BankAccount(**payload.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.get("/{account_id}", response_model=BankAccountRead)
def get_bank_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(BankAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return account


@router.patch("/{account_id}", response_model=BankAccountRead)
def update_bank_account(account_id: int, payload: BankAccountUpdate, db: Session = Depends(get_db)):
    account = db.get(BankAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(account, field, value)

    db.commit()
    db.refresh(account)
    return account


@router.delete("/{account_id}", status_code=204)
def delete_bank_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(BankAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    db.delete(account)
    db.commit()