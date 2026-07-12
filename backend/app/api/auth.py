from datetime import datetime, timedelta
import uuid

from fastapi import APIRouter, Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from sqlalchemy.orm import Session
from jwt import encode, decode
from passlib.context import CryptContext

from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserLoginRequest,
    UserLoginResponse,
    UserResponse,
)
from app.config import settings
from app.middleware.error_handler import (
    ValidationError,
    AuthenticationError,
)

router = APIRouter(tags=["Authentication"])

security = HTTPBearer()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


@router.post(
    "/register",
    response_model=UserResponse,
)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise ValidationError(
            "User with this email already exists"
        )

    new_user = User(
        id=str(uuid.uuid4()),
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(
            user_data.password
        ),
        role=user_data.role,
        is_active=True,
        is_verified=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post(
    "/login",
    response_model=UserLoginResponse,
)
async def login(
    credentials: UserLoginRequest,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == credentials.email)
        .first()
    )

    if not user:
        raise AuthenticationError(
            "Invalid email or password"
        )

    if not verify_password(
        credentials.password,
        user.hashed_password,
    ):
        raise AuthenticationError(
            "Invalid email or password"
        )

    if not user.is_active:
        raise AuthenticationError(
            "User account is inactive"
        )

    user.last_login = datetime.utcnow()

    db.commit()
    db.refresh(user)

    payload = {
        "sub": user.id,
        "email": user.email,
        "role": user.role.value,
        "exp": datetime.utcnow()
        + timedelta(
            hours=settings.JWT_EXPIRATION_HOURS
        ),
        "iat": datetime.utcnow(),
    }

    access_token = encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return UserLoginResponse(
        access_token=access_token,
        refresh_token=None,
        token_type="bearer",
        user=user,
    )


async def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db),
):
    try:
        payload = decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM
            ],
        )

        user_id = payload.get("sub")

        if not user_id:
            raise AuthenticationError(
                "Invalid token"
            )

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise AuthenticationError(
                "User not found"
            )

        return user

    except Exception:
        raise AuthenticationError(
            "Invalid token"
        )


@router.get(
    "/me",
    response_model=UserResponse,
)
async def me(
    current_user: User = Depends(
        get_authenticated_user
    ),
):
    return current_user


@router.post("/logout")
async def logout():
    return {
        "message": "Logged out successfully"
    }