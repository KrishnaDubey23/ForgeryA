from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np


@dataclass
class ROIResult:
    kind: str
    bbox: Tuple[int, int, int, int]  # x, y, w, h
    path: str


def _save_crop(image: np.ndarray, bbox: Tuple[int, int, int, int], path: Path) -> str:
    x, y, w, h = bbox
    crop = image[y : y + h, x : x + w]
    path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(path), crop)
    return str(path)


def detect_face_rois(image: np.ndarray, base_dir: Path) -> List[ROIResult]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        str(Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml")
    )
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    results: List[ROIResult] = []
    for i, (x, y, w, h) in enumerate(faces):
        path = base_dir / f"face_{i}.jpg"
        saved = _save_crop(image, (x, y, w, h), path)
        results.append(ROIResult(kind="face", bbox=(x, y, w, h), path=saved))
    return results


def detect_text_block_rois(image: np.ndarray, base_dir: Path) -> List[ROIResult]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh = 255 - thresh

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 5))
    dilated = cv2.dilate(thresh, kernel, iterations=2)

    contours, _ = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    results: List[ROIResult] = []
    for i, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        if w * h < 500:
            continue
        aspect = w / float(h)
        if aspect < 1.5:
            continue
        path = base_dir / f"text_{i}.jpg"
        saved = _save_crop(image, (x, y, w, h), path)
        results.append(ROIResult(kind="text", bbox=(x, y, w, h), path=saved))
    return results


def detect_qr_rois(image: np.ndarray, base_dir: Path) -> List[ROIResult]:
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(image)
    results: List[ROIResult] = []
    if points is not None and len(points) > 0:
        pts = points[0].astype(int)
        x, y, w, h = cv2.boundingRect(pts)
        path = base_dir / "qr_0.jpg"
        saved = _save_crop(image, (x, y, w, h), path)
        results.append(ROIResult(kind="qr", bbox=(x, y, w, h), path=saved))
    return results


def detect_all_rois(image_path: str, output_dir: str) -> List[ROIResult]:
    """
    Detect ROIs (face, QR, text blocks) and save crops.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to read image at {image_path}")

    base_dir = Path(output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    rois: List[ROIResult] = []
    rois.extend(detect_face_rois(img, base_dir / "faces"))
    rois.extend(detect_qr_rois(img, base_dir / "qr"))
    rois.extend(detect_text_block_rois(img, base_dir / "text"))
    return rois

