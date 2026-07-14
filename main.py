import logging

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from app.database import Base, engine, get_db
from app.models import User
from app.operations import add, divide, multiply, subtract
from app.schemas import UserCreate, UserRead


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI Secure Users Calculator")

# Creates any SQLAlchemy tables that do not already exist.
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator("a", "b")
    @classmethod
    def validate_numbers(cls, value: float) -> float:
        if not isinstance(value, (int, float)):
            raise ValueError("Both a and b must be numbers.")
        return value


class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    logger.error(
        "HTTP exception on %s: %s",
        request.url.path,
        exc.detail,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    error_messages = "; ".join(
        f"{error['loc'][-1]}: {error['msg']}"
        for error in exc.errors()
    )

    logger.error(
        "Validation error on %s: %s",
        request.url.path,
        error_messages,
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": error_messages},
    )


@app.get("/")
async def read_root(request: Request):
    """Serve the calculator webpage."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> User:
    """Create a user while storing only the password hash."""
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    try:
        user = create_user(db, user_data)
        logger.info("Created user: %s", user.username)
        return user
    except IntegrityError as error:
        db.rollback()
        logger.error("Database integrity error: %s", error)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists",
        ) from error


@app.get(
    "/users/{username}",
    response_model=UserRead,
)
def read_user(
    username: str,
    db: Session = Depends(get_db),
) -> User:
    """Retrieve a user without returning the password hash."""
    user = get_user_by_username(db, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@app.post(
    "/add",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def add_route(operation: OperationRequest) -> OperationResponse:
    try:
        return OperationResponse(
            result=add(operation.a, operation.b)
        )
    except Exception as error:
        logger.error("Add operation error: %s", error)
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.post(
    "/subtract",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def subtract_route(operation: OperationRequest) -> OperationResponse:
    try:
        return OperationResponse(
            result=subtract(operation.a, operation.b)
        )
    except Exception as error:
        logger.error("Subtract operation error: %s", error)
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.post(
    "/multiply",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}},
)
async def multiply_route(operation: OperationRequest) -> OperationResponse:
    try:
        return OperationResponse(
            result=multiply(operation.a, operation.b)
        )
    except Exception as error:
        logger.error("Multiply operation error: %s", error)
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error


@app.post(
    "/divide",
    response_model=OperationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def divide_route(operation: OperationRequest) -> OperationResponse:
    try:
        return OperationResponse(
            result=divide(operation.a, operation.b)
        )
    except ValueError as error:
        logger.error("Divide operation error: %s", error)
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
    except Exception as error:
        logger.exception("Unexpected division error: %s", error)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        ) from error


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )