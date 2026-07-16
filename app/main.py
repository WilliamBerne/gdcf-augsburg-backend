# app/main.py

from app.config import load_env
load_env()

from fastapi import FastAPI
from app.db import engine

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}
