import pytest


def create_member(client):
    response = client.post(
        "/members/",
        json={
            "last_name": "Mustermann",
            "first_name": "Erika",
            "membership_type": "single",
            "street": "Musterstrasse 1",
            "postal_code": "86150",
            "city": "Augsburg",
            "email": "erika@example.com",
        },
    )
    assert response.status_code == 201
    return response.json()


def bank_account_payload(member_id, **overrides):
    payload = {
        "member_id": member_id,
        "account_holder_name": "Erika Mustermann",
        "street": "Musterstrasse 1",
        "postal_code": "86150",
        "city": "Augsburg",
        "bank_name": "Test Bank",
        "iban": "DE89370400440532013000",
    }
    payload.update(overrides)
    return payload


def create_bank_account(client, member_id, **overrides):
    response = client.post(
        "/bank-accounts/",
        json=bank_account_payload(member_id, **overrides),
    )
    assert response.status_code == 201
    return response.json()


def test_create_and_get_bank_account(client):
    member = create_member(client)
    created = create_bank_account(client, member["id"])

    response = client.get(f"/bank-accounts/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_create_bank_account_with_only_required_fields(client):
    member = create_member(client)

    response = client.post(
        "/bank-accounts/",
        json={
            "member_id": member["id"],
            "account_holder_name": "Erika Mustermann",
            "iban": "DE89370400440532013000",
        },
    )

    assert response.status_code == 201
    assert response.json()["street"] is None
    assert response.json()["postal_code"] is None
    assert response.json()["city"] is None
    assert response.json()["bank_name"] is None


def test_update_bank_account(client):
    member = create_member(client)
    created = create_bank_account(client, member["id"])

    response = client.patch(
        f"/bank-accounts/{created['id']}",
        json={"bank_name": "New Bank", "city": "Friedberg"},
    )

    assert response.status_code == 200
    assert response.json()["bank_name"] == "New Bank"
    assert response.json()["city"] == "Friedberg"
    assert response.json()["iban"] == created["iban"]


@pytest.mark.parametrize("field", ["street", "postal_code", "city", "bank_name"])
def test_update_bank_account_can_clear_optional_field(client, field):
    member = create_member(client)
    account = create_bank_account(client, member["id"])

    response = client.patch(
        f"/bank-accounts/{account['id']}",
        json={field: None},
    )

    assert response.status_code == 200
    assert response.json()[field] is None


@pytest.mark.parametrize("field", ["account_holder_name", "iban"])
def test_update_bank_account_rejects_null_required_field(client, field):
    member = create_member(client)
    account = create_bank_account(client, member["id"])

    response = client.patch(
        f"/bank-accounts/{account['id']}",
        json={field: None},
    )

    assert response.status_code == 422

    unchanged = client.get(f"/bank-accounts/{account['id']}")
    assert unchanged.status_code == 200
    assert unchanged.json()[field] == account[field]


def test_delete_bank_account_preserves_member(client):
    member = create_member(client)
    account = create_bank_account(client, member["id"])

    response = client.delete(f"/bank-accounts/{account['id']}")

    assert response.status_code == 204
    assert client.get(f"/bank-accounts/{account['id']}").status_code == 404
    assert client.get(f"/members/{member['id']}").status_code == 200


def test_bank_account_requires_existing_member(client):
    response = client.post(
        "/bank-accounts/",
        json=bank_account_payload(member_id=999),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Member not found"


def test_member_cannot_have_two_bank_accounts(client):
    member = create_member(client)
    create_bank_account(client, member["id"])

    response = client.post(
        "/bank-accounts/",
        json=bank_account_payload(member["id"], bank_name="Another Bank"),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "This member already has a bank account on file"


def test_incomplete_bank_account_payload_is_rejected(client):
    member = create_member(client)
    payload = bank_account_payload(member["id"])
    del payload["iban"]

    response = client.post("/bank-accounts/", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_missing_bank_account_returns_not_found(client, method):
    request = getattr(client, method)
    kwargs = {"json": {"city": "Augsburg"}} if method == "patch" else {}

    response = request("/bank-accounts/999", **kwargs)

    assert response.status_code == 404
    assert response.json()["detail"] == "Bank account not found"
