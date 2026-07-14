import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.crud import create_calculation, create_user
from app.models import Calculation
from app.schemas import (
    CalculationCreate,
    CalculationType,
    UserCreate,
)


def test_create_calculation(db_session):
    unique = uuid.uuid4().hex[:8]

    user = create_user(
        db_session,
        UserCreate(
            username=f"user_{unique}",
            email=f"user_{unique}@example.com",
            password="Password123!",
        ),
    )

    calculation = create_calculation(
        db_session,
        CalculationCreate(
            a=8,
            b=2,
            type=CalculationType.DIVIDE,
            user_id=user.id,
        ),
    )

    stored = (
        db_session.query(Calculation)
        .filter(Calculation.id == calculation.id)
        .first()
    )

    assert stored is not None
    assert stored.a == 8
    assert stored.b == 2
    assert stored.type == CalculationType.DIVIDE.value
    assert stored.result == 4
    assert stored.user_id == user.id


def test_calculation_requires_valid_user(db_session):
    calculation = CalculationCreate(
        a=2,
        b=3,
        type=CalculationType.ADD,
        user_id=999999,
    )

    with pytest.raises(IntegrityError):
        create_calculation(db_session, calculation)

    db_session.rollback()