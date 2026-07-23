import pytest


def member_payload(**overrides):
    payload = {
        "last_name": "Mustermann",
        "first_name": "Erika",
        "membership_type": "single",
        "street": "Musterstrasse 1",
        "postal_code": "86150",
        "city": "Augsburg",
        "email": "erika@example.com",
    }
    payload.update(overrides)
    return payload


def create_member(client, **overrides):
    response = client.post("/members/", json=member_payload(**overrides))
    assert response.status_code == 201
    return response.json()


def test_create_and_get_member(client):
    created = create_member(client)

    response = client.get(f"/members/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_list_members(client):
    first = create_member(client)
    second = create_member(
        client,
        first_name="Max",
        email="max@example.com",
    )

    response = client.get("/members/")

    assert response.status_code == 200
    assert response.json() == [first, second]


def test_update_member(client):
    created = create_member(client)

    response = client.patch(
        f"/members/{created['id']}",
        json={"city": "Friedberg", "membership_type": "family"},
    )

    assert response.status_code == 200
    assert response.json()["city"] == "Friedberg"
    assert response.json()["membership_type"] == "family"
    assert response.json()["email"] == created["email"]


def test_delete_member(client):
    created = create_member(client)

    response = client.delete(f"/members/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/members/{created['id']}").status_code == 404


def test_duplicate_email_is_rejected(client):
    create_member(client)

    response = client.post("/members/", json=member_payload())

    assert response.status_code == 409
    assert response.json()["detail"] == "A member with this email already exists"


@pytest.mark.parametrize(
    "payload",
    [
        member_payload(email="not-an-email"),
        {key: value for key, value in member_payload().items() if key != "last_name"},
        member_payload(membership_type="unknown"),
    ],
)
def test_invalid_member_payload_is_rejected(client, payload):
    response = client.post("/members/", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_missing_member_returns_not_found(client, method):
    request = getattr(client, method)
    kwargs = {"json": {"city": "Augsburg"}} if method == "patch" else {}

    response = request("/members/999", **kwargs)

    assert response.status_code == 404
    assert response.json()["detail"] == "Member not found"
