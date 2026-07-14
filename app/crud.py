from sqlalchemy import select
from sqlalchemy.orm import Session

from app.calculation_factory import CalculationFactory
from app.models import Calculation, User
from app.schemas import CalculationCreate, UserCreate
from app.security import hash_password


# -------------------------
# User CRUD
# -------------------------

def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:
    statement = select(User).where(User.username == username)
    return db.scalar(statement)


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    statement = select(User).where(User.email == email)
    return db.scalar(statement)


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# -------------------------
# Calculation CRUD
# -------------------------

def create_calculation(
    db: Session,
    calculation_data: CalculationCreate,
) -> Calculation:
    operation = CalculationFactory.create(
        calculation_data.type,
    )

    result = operation.calculate(
        calculation_data.a,
        calculation_data.b,
    )

    calculation = Calculation(
        a=calculation_data.a,
        b=calculation_data.b,
        type=calculation_data.type.value,
        result=result,
        user_id=calculation_data.user_id,
    )

    db.add(calculation)
    db.commit()
    db.refresh(calculation)

    return calculation


def get_calculation(
    db: Session,
    calculation_id: int,
) -> Calculation | None:
    statement = select(Calculation).where(
        Calculation.id == calculation_id
    )

    return db.scalar(statement)