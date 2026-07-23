import pytest


def create_member(client, email="erika@example.com"):
    response = client.post(
        "/members/",
        json={
            "last_name": "Mustermann",
            "first_name": "Erika",
            "membership_type": "single",
            "street": "Musterstrasse 1",
            "postal_code": "86150",
            "city": "Augsburg",
            "email": email,
        },
    )
    assert response.status_code == 201
    return response.json()


def document_payload(member_id, **overrides):
    payload = {
        "member_id": member_id,
        "document_type": "application",
        "file_path": "members/1/application.pdf",
    }
    payload.update(overrides)
    return payload


def create_document(client, member_id, **overrides):
    response = client.post(
        "/documents/",
        json=document_payload(member_id, **overrides),
    )
    assert response.status_code == 201
    return response.json()


def test_list_documents_for_member_is_not_shadowed_by_document_id_route(client):
    response = client.get("/documents/member/123")

    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_document(client):
    member = create_member(client)
    created = create_document(client, member["id"])

    response = client.get(f"/documents/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created
    assert created["uploaded_at"] is not None


def test_list_documents_only_for_requested_member(client):
    first_member = create_member(client)
    second_member = create_member(client, email="max@example.com")
    first_document = create_document(client, first_member["id"])
    create_document(
        client,
        second_member["id"],
        document_type="consent",
        file_path="members/2/consent.pdf",
    )

    response = client.get(f"/documents/member/{first_member['id']}")

    assert response.status_code == 200
    assert response.json() == [first_document]


def test_delete_document_preserves_member(client):
    member = create_member(client)
    document = create_document(client, member["id"])

    response = client.delete(f"/documents/{document['id']}")

    assert response.status_code == 204
    assert client.get(f"/documents/{document['id']}").status_code == 404
    assert client.get(f"/members/{member['id']}").status_code == 200


def test_document_requires_existing_member(client):
    response = client.post("/documents/", json=document_payload(member_id=999))

    assert response.status_code == 404
    assert response.json()["detail"] == "Member not found"


@pytest.mark.parametrize(
    "payload",
    [
        {"member_id": 1, "document_type": "application"},
        {"member_id": 1, "file_path": "members/1/application.pdf"},
        document_payload(member_id="not-an-integer"),
    ],
)
def test_invalid_document_payload_is_rejected(client, payload):
    response = client.post("/documents/", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize("method", ["get", "delete"])
def test_missing_document_returns_not_found(client, method):
    response = getattr(client, method)("/documents/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"
