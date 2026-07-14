from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    created_at: datetime


class CalculationType(str, Enum):
    ADD = "Add"
    SUBTRACT = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"


class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalculationType
    user_id: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_division(self):
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Division by zero is not allowed.")
        return self


class CalculationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    a: float
    b: float
    type: CalculationType
    result: float
    user_id: int
    created_at: datetime