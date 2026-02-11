import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

from .densenet import DenseNet121Binary, load_densenet_checkpoint
from .mobilenet import MobileNetV2Binary, load_mobilenet_checkpoint
from .ensemble import EnsembleScores, compute_ensemble
from .gradcam import GradCAM, overlay_heatmap_on_image


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


transform = transforms.Compose(
    [
        transforms.Resize((384, 384)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ]
)


@dataclass
class ROIInferenceResult:
    kind: str
    path: str
    scores: EnsembleScores
    heatmap_path: str


@dataclass
class InferenceResult:
    full_image_scores: EnsembleScores
    full_image_heatmap: str
    roi_results: List[ROIInferenceResult]
    tampered_ratio: float
    severity: str


def _load_image_tensor(image_path: str) -> torch.Tensor:
    img = Image.open(image_path).convert("RGB")
    t = transform(img).unsqueeze(0)
    return t.to(device)


def _compute_tampered_ratio(heatmaps: List[np.ndarray], threshold: float = 0.5) -> float:
    if not heatmaps:
        return 0.0
    masks = [(h >= threshold).astype(np.float32) for h in heatmaps]
    total_on = sum(m.sum() for m in masks)
    total_pixels = sum(m.size for m in masks)
    if total_pixels == 0:
        return 0.0
    return float(total_on / total_pixels)


def classify_severity(ensemble_score: float, tampered_ratio: float) -> str:
    """
    Map ensemble probability and tampered heatmap area ratio to severity label.
    """
    if ensemble_score < 0.3 and tampered_ratio < 0.15:
        return "Authentic"
    if ensemble_score < 0.5 and tampered_ratio < 0.3:
        return "Minor Tampering"
    if ensemble_score < 0.75 and tampered_ratio < 0.6:
        return "Partial Forgery"
    return "Complete Forgery"


class ForgeryInferencePipeline:
    def __init__(self, checkpoint_dir: str, storage_dir: str):
        self.checkpoint_dir = checkpoint_dir
        self.storage_dir = storage_dir

        self.densenet: DenseNet121Binary = load_densenet_checkpoint(
            checkpoint_dir, device
        )
        self.mobilenet: MobileNetV2Binary = load_mobilenet_checkpoint(
            checkpoint_dir, device
        )

        # Target layers for Grad-CAM
        self.densenet_cam = GradCAM(
            self.densenet.model.features, self.densenet.model.features[-1]
        )
        self.mobilenet_cam = GradCAM(
            self.mobilenet.model.features, self.mobilenet.model.features[-1]
        )

    def _infer_single(
        self, image_path: str, heatmap_dir: str
    ) -> (EnsembleScores, str, np.ndarray):
        tensor = _load_image_tensor(image_path)

        with torch.no_grad():
            dn_logit = self.densenet(tensor).item()
            mb_logit = self.mobilenet(tensor).item()

        scores = compute_ensemble(dn_logit, mb_logit)

        # Use DenseNet Grad-CAM as reference heatmap
        heatmap = self.densenet_cam.generate(tensor)
        heatmap_path = overlay_heatmap_on_image(
            image_path, heatmap, os.path.join(heatmap_dir, "heatmap.jpg")
        )

        return scores, heatmap_path, heatmap

    def run(
        self,
        full_image_path: str,
        roi_paths: Optional[List[Dict]] = None,
        upload_id: Optional[str] = None,
    ) -> InferenceResult:
        """
        Run inference on full image and ROIs.
        roi_paths: list of dicts with keys {kind, path}
        """
        base_heatmap_dir = Path(self.storage_dir) / "heatmaps"
        if upload_id:
            base_heatmap_dir = base_heatmap_dir / upload_id
        base_heatmap_dir.mkdir(parents=True, exist_ok=True)

        full_scores, full_heatmap_path, full_heatmap = self._infer_single(
            full_image_path, str(base_heatmap_dir / "full")
        )

        roi_results: List[ROIInferenceResult] = []
        roi_heatmaps: List[np.ndarray] = [full_heatmap]

        if roi_paths:
            for i, roi in enumerate(roi_paths):
                kind = roi.get("kind", "roi")
                path = roi["path"]
                scores, heatmap_path, heatmap = self._infer_single(
                    path, str(base_heatmap_dir / f"roi_{i}")
                )
                roi_results.append(
                    ROIInferenceResult(
                        kind=kind,
                        path=path,
                        scores=scores,
                        heatmap_path=heatmap_path,
                    )
                )
                roi_heatmaps.append(heatmap)

        tampered_ratio = _compute_tampered_ratio(roi_heatmaps)
        severity = classify_severity(full_scores.ensemble, tampered_ratio)

        return InferenceResult(
            full_image_scores=full_scores,
            full_image_heatmap=full_heatmap_path,
            roi_results=roi_results,
            tampered_ratio=tampered_ratio,
            severity=severity,
        )

