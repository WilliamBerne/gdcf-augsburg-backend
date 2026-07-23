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


def create_document(client, member_id, file_path="members/1/consent.pdf"):
    response = client.post(
        "/documents/",
        json={
            "member_id": member_id,
            "document_type": "consent",
            "file_path": file_path,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_new_consent_starts_pending_human_review(client):
    member = create_member(client)

    consent = create_consent(client, member["id"])

    assert consent["form_version"] == "gdcf-consent-de-zh-v1"
    assert consent["data_protection_signature_status"] == "pending_review"
    assert consent["photo_video_signature_status"] == "pending_review"
    assert consent["data_protection_reviewed_at"] is None
    assert consent["photo_video_reviewed_at"] is None


def test_verify_and_reset_signature_review(client):
    member = create_member(client)
    consent = create_consent(client, member["id"])

    verified = client.patch(
        f"/consents/{consent['id']}",
        json={
            "data_protection_signature_status": "verified",
            "data_protection_reviewed_by": "Board Member",
            "data_protection_signer_role": "member",
        },
    )

    assert verified.status_code == 200
    assert verified.json()["data_protection_signature_status"] == "verified"
    assert verified.json()["data_protection_reviewed_by"] == "Board Member"
    assert verified.json()["data_protection_reviewed_at"] is not None

    pending = client.patch(
        f"/consents/{consent['id']}",
        json={"data_protection_signature_status": "pending_review"},
    )

    assert pending.status_code == 200
    assert pending.json()["data_protection_reviewed_by"] is None
    assert pending.json()["data_protection_reviewed_at"] is None


@pytest.mark.parametrize("status", ["verified", "missing", "unclear"])
def test_completed_review_requires_reviewer(client, status):
    member = create_member(client)
    consent = create_consent(client, member["id"])

    response = client.patch(
        f"/consents/{consent['id']}",
        json={"photo_video_signature_status": status},
    )

    assert response.status_code == 422


def test_consent_can_link_signed_document_for_same_member(client):
    member = create_member(client)
    document = create_document(client, member["id"])

    consent = create_consent(
        client,
        member["id"],
        signed_document_id=document["id"],
        photo_video_minor_co_signed=True,
    )

    assert consent["signed_document_id"] == document["id"]
    assert consent["photo_video_minor_co_signed"] is True


def test_consent_rejects_signed_document_from_other_member(client):
    member = create_member(client)
    other_member = create_member(client)
    document = create_document(client, other_member["id"], "members/2/consent.pdf")

    response = client.post(
        "/consents/",
        json=consent_payload(member["id"], signed_document_id=document["id"]),
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Signed document belongs to a different member"


@pytest.mark.parametrize(
    ("field", "timestamp_field"),
    [
        ("data_protection_consent", "data_protection_withdrawn_at"),
        ("newsletter_opt_in", "newsletter_withdrawn_at"),
    ],
)
def test_withdraw_and_regrant_consent_tracks_timestamp(client, field, timestamp_field):
    member = create_member(client)
    consent = create_consent(client, member["id"])

    withdrawn = client.patch(
        f"/consents/{consent['id']}",
        json={field: False},
    )

    assert withdrawn.status_code == 200
    assert withdrawn.json()[timestamp_field] is not None

    regranted = client.patch(
        f"/consents/{consent['id']}",
        json={field: True},
    )

    assert regranted.status_code == 200
    assert regranted.json()[timestamp_field] is None


@pytest.mark.parametrize(
    "field",
    [
        "data_protection_consent",
        "data_protection_signature_status",
        "newsletter_opt_in",
        "photo_video_consent",
        "photo_video_signature_status",
    ],
)
def test_consent_update_rejects_null_required_field(client, field):
    member = create_member(client)
    consent = create_consent(client, member["id"])

    response = client.patch(
        f"/consents/{consent['id']}",
        json={field: None},
    )

    assert response.status_code == 422
    assert client.get(f"/consents/{consent['id']}").status_code == 200
