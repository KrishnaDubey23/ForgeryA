"""
Mock inference pipeline for testing without trained models.
Returns realistic dummy predictions when actual models aren't available.
"""
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


@dataclass
class EnsembleScores:
    densenet: float
    mobilenet: float
    ensemble: float


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


def classify_severity(ensemble_score: float, tampered_ratio: float) -> str:
    """Map ensemble probability and tampered heatmap area ratio to severity label."""
    if ensemble_score < 0.3 and tampered_ratio < 0.15:
        return "Authentic"
    if ensemble_score < 0.5 and tampered_ratio < 0.3:
        return "Minor Tampering"
    if ensemble_score < 0.75 and tampered_ratio < 0.6:
        return "Partial Forgery"
    return "Complete Forgery"


def create_mock_heatmap(image_path: str, heatmap_path: str, tampering_intensity: float = 0.5) -> str:
    """Create a mock heatmap visualization."""
    try:
        # Open original image
        img = Image.open(image_path).convert("RGB")
        width, height = img.size
        
        # Create heatmap overlay
        heatmap = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(heatmap)
        
        # Add random colored regions based on tampering intensity
        num_regions = max(1, int(5 * tampering_intensity))
        for _ in range(num_regions):
            x1 = random.randint(0, width - 50)
            y1 = random.randint(0, height - 50)
            x2 = x1 + random.randint(50, min(200, width - x1))
            y2 = y1 + random.randint(50, min(200, height - y1))
            
            # Red for high confidence tampering
            opacity = int(200 * tampering_intensity)
            draw.rectangle([x1, y1, x2, y2], fill=(255, 50, 50, opacity))
            draw.rectangle([x1, y1, x2, y2], outline=(255, 100, 100, 255), width=2)
        
        # Blend heatmap with original image
        result = img.convert("RGBA")
        result = Image.alpha_composite(result, heatmap)
        result = result.convert("RGB")
        
        # Save
        result.save(heatmap_path)
        return heatmap_path
    except Exception as e:
        print(f"Error creating heatmap: {e}")
        return heatmap_path


class MockInferencePipeline:
    """Mock pipeline that returns realistic dummy predictions."""
    
    def __init__(self, checkpoint_dir: str, storage_dir: str):
        self.checkpoint_dir = checkpoint_dir
        self.storage_dir = storage_dir
        print(f"[MOCK MODE] Using mock inference pipeline (no trained models available)")
    
    def run(
        self,
        full_image_path: str,
        roi_paths: Optional[List[Dict]] = None,
        upload_id: Optional[str] = None,
    ) -> InferenceResult:
        """Generate mock inference results with same interface as real pipeline."""
        
        # Create heatmap directory
        base_heatmap_dir = Path(self.storage_dir) / "heatmaps"
        if upload_id:
            base_heatmap_dir = base_heatmap_dir / upload_id
        base_heatmap_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate random scores that seem realistic
        # Mostly show authentic documents with occasional forgeries
        random_seed = random.random()
        if random_seed < 0.7:  # 70% authentic
            densenet_score = random.uniform(0.05, 0.25)
            mobilenet_score = random.uniform(0.05, 0.25)
            tampering_ratio = random.uniform(0.01, 0.15)
        elif random_seed < 0.85:  # 15% minor tampering
            densenet_score = random.uniform(0.25, 0.45)
            mobilenet_score = random.uniform(0.25, 0.45)
            tampering_ratio = random.uniform(0.15, 0.35)
        elif random_seed < 0.95:  # 10% partial forgery
            densenet_score = random.uniform(0.45, 0.70)
            mobilenet_score = random.uniform(0.45, 0.70)
            tampering_ratio = random.uniform(0.35, 0.60)
        else:  # 5% complete forgery
            densenet_score = random.uniform(0.70, 0.99)
            mobilenet_score = random.uniform(0.70, 0.99)
            tampering_ratio = random.uniform(0.60, 0.95)
        
        ensemble_score = (densenet_score + mobilenet_score) / 2
        severity = classify_severity(ensemble_score, tampering_ratio)
        
        # Create full image heatmap
        heatmap_full_dir = base_heatmap_dir / "full"
        heatmap_full_dir.mkdir(parents=True, exist_ok=True)
        heatmap_full_path = str(heatmap_full_dir / "heatmap.jpg")
        create_mock_heatmap(full_image_path, heatmap_full_path, ensemble_score)
        
        # Create mock ROI results if ROI paths provided
        roi_results = []
        if roi_paths:
            for i, roi in enumerate(roi_paths):
                roi_path = roi.get("path", "")
                roi_kind = roi.get("kind", "unknown")
                
                # Generate scores for this ROI
                roi_dens = random.uniform(max(0.0, densenet_score - 0.15), min(1.0, densenet_score + 0.15))
                roi_mobile = random.uniform(max(0.0, mobilenet_score - 0.15), min(1.0, mobilenet_score + 0.15))
                roi_scores = EnsembleScores(
                    densenet=roi_dens,
                    mobilenet=roi_mobile,
                    ensemble=(roi_dens + roi_mobile) / 2
                )
                
                # Create ROI heatmap
                roi_heatmap_dir = base_heatmap_dir / f"roi_{i}"
                roi_heatmap_dir.mkdir(parents=True, exist_ok=True)
                roi_heatmap_path = str(roi_heatmap_dir / "heatmap.jpg")
                if os.path.exists(roi_path):
                    create_mock_heatmap(roi_path, roi_heatmap_path, roi_scores.ensemble)
                
                roi_results.append(ROIInferenceResult(
                    kind=roi_kind,
                    path=roi_path,
                    scores=roi_scores,
                    heatmap_path=roi_heatmap_path
                ))
        
        return InferenceResult(
            full_image_scores=EnsembleScores(
                densenet=densenet_score,
                mobilenet=mobilenet_score,
                ensemble=ensemble_score
            ),
            full_image_heatmap=heatmap_full_path,
            roi_results=roi_results,
            tampered_ratio=tampering_ratio,
            severity=severity
        )
