from pydantic import ValidationError

from app.schemas import UserCreate


def test_valid_user():
    user = UserCreate(
        username="john",
        email="john@example.com",
        password="Password123!"
    )

    assert user.username == "john"
    assert user.email == "john@example.com"


def test_invalid_email():
    try:
        UserCreate(
            username="john",
            email="not-an-email",
            password="Password123!"
        )

        assert False

    except ValidationError:
        assert True


def test_short_password():
    try:
        UserCreate(
            username="john",
            email="john@example.com",
            password="123"
        )

        assert False

    except ValidationError:
        assert True