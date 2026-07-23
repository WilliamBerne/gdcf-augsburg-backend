# app/api/routers/document.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.member import Member
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentRead

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/", response_model=DocumentRead, status_code=201)
def create_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    member = db.get(Member, payload.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    document = Document(**payload.model_dump())
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@router.get("/member/{member_id}", response_model=list[DocumentRead])
def list_documents_for_member(member_id: int, db: Session = Depends(get_db)):
    return db.query(Document).filter(Document.member_id == member_id).all()


@router.get("/{document_id}", response_model=DocumentRead)
def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}", status_code=204)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(document)
    db.commit()