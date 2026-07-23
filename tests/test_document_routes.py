import os

from fastapi.testclient import TestClient


os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_NAME", "test")

from app.api.deps import get_db
from app.main import app


class EmptyDocumentQuery:
    def filter(self, *_args):
        return self

    def all(self):
        return []


class FakeDatabase:
    def query(self, _model):
        return EmptyDocumentQuery()


def override_get_db():
    yield FakeDatabase()


def test_list_documents_for_member_is_not_shadowed_by_document_id_route():
    app.dependency_overrides[get_db] = override_get_db

    try:
        response = TestClient(app).get("/documents/member/123")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == []
