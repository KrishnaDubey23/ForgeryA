from dataclasses import dataclass
from typing import Dict, List

import numpy as np


@dataclass
class EnsembleScores:
    densenet: float
    mobilenet: float
    ensemble: float


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def compute_ensemble(
    densenet_logit: float,
    mobilenet_logit: float,
    weight_densenet: float = 0.6,
    weight_mobilenet: float = 0.4,
) -> EnsembleScores:
    """
    Compute weighted ensemble from DenseNet and MobileNet logits.

    Returns scores in [0, 1] interpreted as probability of forgery.
    """
    dn = sigmoid(float(densenet_logit))
    mb = sigmoid(float(mobilenet_logit))
    total = weight_densenet + weight_mobilenet
    wd = weight_densenet / total
    wm = weight_mobilenet / total
    ensemble = wd * dn + wm * mb
    return EnsembleScores(densenet=dn, mobilenet=mb, ensemble=ensemble)


def summarize_roi_scores(
    roi_scores: List[EnsembleScores],
) -> Dict[str, float]:
    """
    Aggregate ROI-level ensemble scores.
    """
    if not roi_scores:
        return {"max": 0.0, "mean": 0.0}
    arr = np.array([r.ensemble for r in roi_scores], dtype=np.float32)
    return {"max": float(arr.max()), "mean": float(arr.mean())}

