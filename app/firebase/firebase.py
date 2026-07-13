import base64
import json
from functools import lru_cache

import firebase_admin
from fastapi import HTTPException, status
from firebase_admin import auth, credentials

from app.core.config import settings


@lru_cache(maxsize=1)
def get_firebase_app() -> firebase_admin.App:
    if not settings.FIREBASE_SERVICE_ACCOUNT_BASE64:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Firebase service account is not configured",
        )

    try:
        service_account_json = base64.b64decode(settings.FIREBASE_SERVICE_ACCOUNT_BASE64).decode("utf-8")
        service_account = json.loads(service_account_json)
    except (ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Firebase service account is invalid",
        ) from exc

    if firebase_admin._apps:
        return firebase_admin.get_app()

    return firebase_admin.initialize_app(credentials.Certificate(service_account))


def verify_google_id_token(id_token: str) -> dict:
    try:
        return auth.verify_id_token(id_token, app=get_firebase_app())
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google sign-in token",
        ) from exc
