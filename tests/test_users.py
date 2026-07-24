import pytest
from pydantic import ValidationError

from app.models.member import Member
from app.models.user import MEMBERSHIP_ROLES, User
from app.schemas.user import UserCreate, UserRead


def member_record():
    return Member(
        last_name="Mustermann",
        first_name="Erika",
        membership_type="single",
        street="Musterstrasse 1",
        postal_code="86150",
        city="Augsburg",
    )


def test_membership_roles_are_explicit():
    assert MEMBERSHIP_ROLES == (
        "member",
        "membership_staff",
        "membership_admin",
    )


def test_external_user_can_link_to_one_member(db_session):
    member = member_record()
    user = User(
        email="member@example.com",
        auth_provider="wordpress",
        external_subject="42",
        member=member,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.role == "member"
    assert user.is_active is True
    assert user.member_id == member.id
    assert member.user.id == user.id


@pytest.mark.parametrize("role", MEMBERSHIP_ROLES)
def test_user_schema_accepts_membership_roles(role):
    payload = UserCreate(
        email="login@example.com",
        external_subject="42",
        role=role,
    )

    assert payload.role == role
    assert payload.auth_provider == "wordpress"


def test_user_schema_rejects_unknown_role():
    with pytest.raises(ValidationError):
        UserCreate(
            email="login@example.com",
            external_subject="42",
            role="webmaster",
        )


def test_user_response_contains_identity_but_no_password(db_session):
    user = User(
        email="staff@example.com",
        auth_provider="wordpress",
        external_subject="84",
        role="membership_staff",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response = UserRead.model_validate(user).model_dump()

    assert "password" not in response
    assert "password_hash" not in response
    assert response["auth_provider"] == "wordpress"
    assert response["external_subject"] == "84"
