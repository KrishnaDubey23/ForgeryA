from pathlib import Path
from typing import Tuple

from PIL import Image, ImageChops, ImageEnhance


def compute_ela(
    image_path: str, output_path: str, quality: int = 90
) -> Tuple[str, Image.Image]:
    """
    Perform Error Level Analysis (ELA) on a JPEG image.

    1. Re-save the image at a given JPEG quality.
    2. Compute pixel-wise difference between original and recompressed.
    3. Enhance the difference to highlight tampering artifacts.

    Returns the output path and the enhanced ELA PIL image.
    """
    image_path = str(image_path)
    original = Image.open(image_path).convert("RGB")

    tmp_path = Path(output_path).with_suffix(".ela_tmp.jpg")
    tmp_path.parent.mkdir(parents=True, exist_ok=True)

    original.save(tmp_path, "JPEG", quality=quality)
    recompressed = Image.open(tmp_path).convert("RGB")

    diff = ImageChops.difference(original, recompressed)

    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema]) or 1
    scale = 255.0 / max_diff

    ela_image = ImageEnhance.Brightness(diff).enhance(scale)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    ela_image.save(output_file, "JPEG")

    tmp_path.unlink(missing_ok=True)
    return str(output_file), ela_image

