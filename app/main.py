# app/main.py

from app.config import load_env
load_env()

from fastapi import FastAPI

from app.api.routers import member, bank_account, consent, document

app = FastAPI(title="GDCF Augsburg Member Management")

app.include_router(member.router)
app.include_router(bank_account.router)
app.include_router(consent.router)
app.include_router(document.router)


@app.get("/")
def root():
    return {"status": "ok"}