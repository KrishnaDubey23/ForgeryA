import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import cv2
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from auth.jwt import decode_token
from convex_client import ConvexClient, get_convex_client
from ml.ela import compute_ela
from ml.qr import decode_qr
from ml.roi import ROIResult, detect_all_rois

# Try to import real inference, fall back to mock
try:
    from ml.inference import ForgeryInferencePipeline as RealInferencePipeline
    USE_MOCK_INFERENCE = False
except Exception as e:
    print(f"[WARNING] Could not import real inference pipeline: {e}")
    print("[WARNING] Using mock inference pipeline instead")
    USE_MOCK_INFERENCE = True
    from ml.mock_inference import MockInferencePipeline as RealInferencePipeline


STORAGE_DIR = Path(os.getenv("STORAGE_DIR", "storage/uploads"))
CHECKPOINT_DIR = os.getenv("MODEL_CHECKPOINT_DIR", "ml/checkpoints")
security = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/predictions", tags=["predictions"])


class PredictionRequest(BaseModel):
    uploadId: str


class ROIMetadata(BaseModel):
    kind: str
    path: str


class PredictionResponse(BaseModel):
    uploadId: str
    densenetScore: float
    mobilenetScore: float
    ensembleScore: float
    severity: str
    tamperedRatio: float
    elaPath: str
    roiCrops: List[ROIMetadata]
    heatmapFull: str
    roiHeatmaps: List[ROIMetadata]
    qrData: Optional[str] = None
    qrValid: bool
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


@router.post("/", response_model=PredictionResponse)
async def run_prediction(
    body: PredictionRequest,
    user_id: str = Depends(get_user_id_from_auth),
    convex: ConvexClient = Depends(get_convex_client),
):
    upload = await convex.query(
        "uploads:getUploadById", {"uploadId": body.uploadId}
    )
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Upload not found"
        )
    if upload["userId"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not your upload"
        )

    image_path = upload["imagePath"]
    if not Path(image_path).exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Uploaded image missing on server"
        )

    # ELA
    ela_dir = STORAGE_DIR / "ela" / body.uploadId
    ela_dir.mkdir(parents=True, exist_ok=True)
    ela_path, _ = compute_ela(
        image_path, str(ela_dir / "ela.jpg")
    )

    # ROI detection
    roi_dir = STORAGE_DIR / "rois" / body.uploadId
    rois: List[ROIResult] = detect_all_rois(image_path, str(roi_dir))

    roi_for_inference = [{"kind": r.kind, "path": r.path} for r in rois]

    # QR validation on full image or QR ROI if exists
    qr_data, qr_valid = decode_qr(image_path)
    if not qr_data:
        # try QR ROI
        qr_rois = [r for r in rois if r.kind == "qr"]
        if qr_rois:
            qr_data, qr_valid = decode_qr(qr_rois[0].path)

    # Inference
    pipeline = RealInferencePipeline(
        CHECKPOINT_DIR, str(STORAGE_DIR)
    )
    result = pipeline.run(
        full_image_path=image_path,
        roi_paths=roi_for_inference,
        upload_id=body.uploadId,
    )

    created_at = datetime.now(timezone.utc).timestamp()

    prediction = await convex.mutation(
        "predictions:createPrediction",
        {
            "uploadId": body.uploadId,
            "densenetScore": result.full_image_scores.densenet,
            "mobilenetScore": result.full_image_scores.mobilenet,
            "ensembleScore": result.full_image_scores.ensemble,
            "severity": result.severity,
            "tamperedRatio": result.tampered_ratio,
            "heatmapPaths": [result.full_image_heatmap]
            + [r.heatmap_path for r in result.roi_results],
            "createdAt": created_at,
        },
    )

    return PredictionResponse(
        uploadId=body.uploadId,
        densenetScore=prediction["densenetScore"],
        mobilenetScore=prediction["mobilenetScore"],
        ensembleScore=prediction["ensembleScore"],
        severity=prediction["severity"],
        tamperedRatio=prediction["tamperedRatio"],
        elaPath=str(ela_path),
        roiCrops=[ROIMetadata(kind=r.kind, path=r.path) for r in rois],
        heatmapFull=result.full_image_heatmap,
        roiHeatmaps=[
            ROIMetadata(kind=r.kind, path=r.heatmap_path) for r in result.roi_results
        ],
        qrData=qr_data,
        qrValid=qr_valid,
        createdAt=prediction["createdAt"],
    )

