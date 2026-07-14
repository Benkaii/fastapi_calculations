import pytest
from pydantic import ValidationError

from app.schemas import CalculationCreate, CalculationType


def test_valid_calculation_create():
    calculation = CalculationCreate(
        a=10,
        b=2,
        type=CalculationType.DIVIDE,
        user_id=1,
    )

    assert calculation.a == 10
    assert calculation.b == 2
    assert calculation.type == CalculationType.DIVIDE
    assert calculation.user_id == 1


def test_invalid_calculation_type():
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=2,
            b=3,
            type="Power",
            user_id=1,
        )


def test_division_by_zero_validation():
    with pytest.raises(
        ValidationError,
        match="Division by zero is not allowed",
    ):
        CalculationCreate(
            a=10,
            b=0,
            type=CalculationType.DIVIDE,
            user_id=1,
        )


def test_invalid_user_id():
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=2,
            b=3,
            type=CalculationType.ADD,
            user_id=0,
        )