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


def consent_payload(member_id, **overrides):
    payload = {
        "member_id": member_id,
        "data_protection_consent": True,
        "data_protection_signed_name": "Erika Mustermann",
        "data_protection_signed_place": "Augsburg",
        "data_protection_signed_date": "2026-07-23",
        "newsletter_opt_in": True,
        "photo_video_consent": False,
    }
    payload.update(overrides)
    return payload


def create_consent(client, member_id, **overrides):
    response = client.post(
        "/consents/",
        json=consent_payload(member_id, **overrides),
    )
    assert response.status_code == 201
    return response.json()


def test_create_and_get_consent(client):
    member = create_member(client)
    created = create_consent(client, member["id"])

    response = client.get(f"/consents/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_update_consent(client):
    member = create_member(client)
    created = create_consent(client, member["id"])

    response = client.patch(
        f"/consents/{created['id']}",
        json={"newsletter_opt_in": False, "photo_video_consent": True},
    )

    assert response.status_code == 200
    assert response.json()["newsletter_opt_in"] is False
    assert response.json()["photo_video_consent"] is True
    assert response.json()["data_protection_consent"] is True


def test_updating_consent_preserves_member(client):
    member = create_member(client)
    consent = create_consent(client, member["id"])

    response = client.patch(
        f"/consents/{consent['id']}",
        json={"data_protection_consent": False},
    )

    assert response.status_code == 200
    assert client.get(f"/members/{member['id']}").status_code == 200


def test_consent_requires_existing_member(client):
    response = client.post("/consents/", json=consent_payload(member_id=999))

    assert response.status_code == 404
    assert response.json()["detail"] == "Member not found"


def test_member_cannot_have_two_consent_records(client):
    member = create_member(client)
    create_consent(client, member["id"])

    response = client.post(
        "/consents/",
        json=consent_payload(member["id"], newsletter_opt_in=False),
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Consent record already exists for this member"


@pytest.mark.parametrize(
    "payload",
    [
        {"newsletter_opt_in": True},
        consent_payload(member_id="not-an-integer"),
        consent_payload(member_id=1, data_protection_signed_date="not-a-date"),
    ],
)
def test_invalid_consent_payload_is_rejected(client, payload):
    response = client.post("/consents/", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize("method", ["get", "patch"])
def test_missing_consent_returns_not_found(client, method):
    request = getattr(client, method)
    kwargs = {"json": {"newsletter_opt_in": False}} if method == "patch" else {}

    response = request("/consents/999", **kwargs)

    assert response.status_code == 404
    assert response.json()["detail"] == "Consent record not found"
