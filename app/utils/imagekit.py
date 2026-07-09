import base64

import requests
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings


def upload_avatar_to_imagekit(file: UploadFile) -> str:
    if not settings.IMAGEKIT_PRIVATE_KEY or not settings.IMAGEKIT_URL_ENDPOINT:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="ImageKit is not configured",
        )

    file_bytes = file.file.read()
    if not file_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")

    encoded_key = base64.b64encode(f"{settings.IMAGEKIT_PRIVATE_KEY}:".encode("utf-8")).decode("utf-8")
    response = requests.post(
        "https://upload.imagekit.io/api/v1/files/upload",
        headers={"Authorization": f"Basic {encoded_key}"},
        data={
            "file": base64.b64encode(file_bytes).decode("utf-8"),
            "fileName": file.filename or "avatar.jpg",
            "folder": "/budget-planner/avatars",
            "useUniqueFileName": "true",
        },
        timeout=30,
    )

    if response.status_code >= 400:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Avatar upload failed")

    return response.json()["url"]
