from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel

from auth.jwt import get_current_admin
from convex_client import ConvexClient, get_convex_client
from ml.train import train_both_models
import os


router = APIRouter(prefix="/admin", tags=["admin"])


class ModelMetric(BaseModel):
    name: str
    version: str
    accuracy: float
    f1Score: float
    createdAt: float


class MetricsResponse(BaseModel):
    models: List[ModelMetric]


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(
    admin_id: str = Depends(get_current_admin),
    convex: ConvexClient = Depends(get_convex_client),
):
    # Fetch user to verify admin status
    user = await convex.query("users:getUserById", {"userId": admin_id})
    if not user or not user.get("isAdmin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )
    models = await convex.query("models:getModelMetrics", {})
    return MetricsResponse(models=models)


def _run_retraining_job(data_dir: str, checkpoint_dir: str):
    train_both_models(data_dir=data_dir, checkpoint_dir=checkpoint_dir)


@router.post("/retrain")
async def trigger_retrain(
    background_tasks: BackgroundTasks,
    admin_id: str = Depends(get_current_admin),
    convex: ConvexClient = Depends(get_convex_client),
):
    """
    Triggers a retraining job and records an admin-only retrain trigger
    in Convex for auditing / orchestration.
    """
    # Fetch user to verify admin status
    user = await convex.query("users:getUserById", {"userId": admin_id})
    if not user or not user.get("isAdmin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required"
        )
    
    timestamp = datetime.now(timezone.utc).timestamp()
    await convex.mutation(
        "models:triggerRetrain",
        {"adminId": admin_id, "triggeredAt": timestamp},
    )

    # Default to ../dataset so a root-level `dataset/` folder is used
    # when the backend is started from the `backend/` directory.
    data_dir = os.getenv("TRAIN_DATA_DIR", "../dataset")
    checkpoint_dir = os.getenv("MODEL_CHECKPOINT_DIR", "ml/checkpoints")
    background_tasks.add_task(_run_retraining_job, data_dir, checkpoint_dir)

    return {"status": "retraining_started", "triggeredAt": timestamp}

