import pytest

from app.calculation_factory import CalculationFactory
from app.schemas import CalculationType


@pytest.mark.parametrize(
    ("calculation_type", "a", "b", "expected"),
    [
        (CalculationType.ADD, 2, 3, 5),
        (CalculationType.SUBTRACT, 10, 4, 6),
        (CalculationType.MULTIPLY, 4, 5, 20),
        (CalculationType.DIVIDE, 10, 2, 5),
    ],
)
def test_factory_operations(
    calculation_type,
    a,
    b,
    expected,
):
    operation = CalculationFactory.create(calculation_type)

    assert operation.calculate(a, b) == expected


def test_division_by_zero():
    operation = CalculationFactory.create(CalculationType.DIVIDE)

    with pytest.raises(
        ValueError,
        match="Division by zero is not allowed",
    ):
        operation.calculate(10, 0)


def test_invalid_calculation_type():
    with pytest.raises(
        ValueError,
        match="Unsupported calculation type",
    ):
        CalculationFactory.create("Invalid")