from typing import Optional, Tuple

import cv2


def decode_qr(image_path: str) -> Tuple[Optional[str], bool]:
    """
    Decode QR code from an image and perform a basic validity check.

    Returns (data, is_valid). For Aadhaar-like QR, you can extend
    the validation logic (prefixes, length, checksum, etc.).
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to read image at {image_path}")

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)
    if not data:
        return None, False

    # Minimal heuristic: non-empty, reasonable length
    is_valid = len(data) > 10
    return data, is_valid

