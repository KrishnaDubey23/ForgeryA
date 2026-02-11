import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from auth.jwt import decode_token
from convex_client import ConvexClient, get_convex_client


STORAGE_DIR = Path(os.getenv("STORAGE_DIR", "storage/uploads"))
security = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/uploads", tags=["uploads"])


class UploadResponse(BaseModel):
    uploadId: str
    imagePath: str
    createdAt: float


def get_user_id_from_auth(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> str:
    """Extract user ID from JWT token. If no token, use demo user."""
    if not credentials:
        return "demo_user_123"
    
    try:
        payload = decode_token(credentials.credentials)
        return payload.get("sub", "demo_user_123")
    except Exception:
        return "demo_user_123"


@router.post("/", response_model=UploadResponse)
async def upload_aadhaar(
    file: UploadFile = File(...),
    user_id: str = Depends(get_user_id_from_auth),
    convex: ConvexClient = Depends(get_convex_client),
):
    try:
        print(f"[UPLOAD] Starting upload for user {user_id}")
        
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="File must be an image"
            )
        timestamp = datetime.now(timezone.utc).timestamp()

        user_dir = STORAGE_DIR / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{int(timestamp)}_{file.filename}"
        file_path = user_dir / filename
        with file_path.open("wb") as f:
            content = await file.read()
            f.write(content)
        
        print(f"[UPLOAD] File saved to {file_path}")

        upload = await convex.mutation(
            "uploads:createUpload",
            {
                "userId": user_id,
                "imagePath": str(file_path),
                "createdAt": timestamp,
            },
        )
        
        print(f"[UPLOAD] Convex response: {upload}")

        return UploadResponse(
            uploadId=str(upload["_id"]),
            imagePath=upload["imagePath"],
            createdAt=upload["createdAt"],
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[UPLOAD ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload error: {str(e)}"
        )

