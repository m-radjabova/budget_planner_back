from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.core.security import hash_password, verify_password
from app.firebase.firebase import verify_google_id_token
from app.models.user import User
from app.schemas.auth import GoogleLoginRequest, LoginRequest, TokenResponse
from app.schemas.user import UserRegister
from app.services.helpers import ensure_email_unique


def register_user(db: Session, payload: UserRegister) -> User:
    ensure_email_unique(db, payload.email)
    user = User(
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, payload: LoginRequest) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return TokenResponse(
        access_token=create_access_token(str(user.id), user.role.value),
        refresh_token=create_refresh_token(str(user.id), user.role.value),
        role=user.role,
    )


def _tokens_for_user(user: User) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(str(user.id), user.role.value),
        refresh_token=create_refresh_token(str(user.id), user.role.value),
        role=user.role,
    )


def login_with_google(db: Session, payload: GoogleLoginRequest) -> TokenResponse:
    decoded_token = verify_google_id_token(payload.id_token)
    firebase_uid = decoded_token.get("uid")
    email = decoded_token.get("email")
    email_verified = decoded_token.get("email_verified")

    if not firebase_uid or not email or not email_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google account email is not verified")

    user = db.scalar(select(User).where(User.firebase_uid == firebase_uid))
    if not user:
        user = db.scalar(select(User).where(User.email == email))

    if user:
        user.firebase_uid = firebase_uid
        user.full_name = user.full_name or decoded_token.get("name") or email.split("@", 1)[0]
        if not user.avatar_url and decoded_token.get("picture"):
            user.avatar_url = decoded_token["picture"]
    else:
        user = User(
            full_name=decoded_token.get("name") or email.split("@", 1)[0],
            email=email,
            hashed_password=hash_password(firebase_uid),
            firebase_uid=firebase_uid,
            avatar_url=decoded_token.get("picture"),
        )
        db.add(user)

    db.commit()
    db.refresh(user)
    return _tokens_for_user(user)


def refresh_user_token(db: Session, refresh_token: str) -> TokenResponse:
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

    user = db.get(User, UUID(payload["sub"]))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return TokenResponse(
        access_token=create_access_token(str(user.id), user.role.value),
        refresh_token=create_refresh_token(str(user.id), user.role.value),
        role=user.role,
    )
