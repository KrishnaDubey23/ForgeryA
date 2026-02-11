from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image


class GradCAM:
    """
    Generic Grad-CAM for torchvision-style CNNs.
    Assumes a final conv feature map followed by pooling + classifier.
    """

    def __init__(self, model: torch.nn.Module, target_layer: torch.nn.Module):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self._hook()

    def _hook(self):
        def forward_hook(module, inp, out):
            self.activations = out.detach()

        def backward_hook(module, grad_in, grad_out):
            self.gradients = grad_out[0].detach()

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_backward_hook(backward_hook)

    def generate(self, input_tensor: torch.Tensor) -> np.ndarray:
        """
        input_tensor: (1, C, H, W)
        Returns heatmap normalized to [0, 1] as numpy array (H, W).
        """
        self.model.zero_grad()
        output = self.model(input_tensor)
        if output.ndim == 1:
            target = output
        else:
            target = output[:, 0]

        target.backward(retain_graph=True)

        gradients = self.gradients  # (N, C, H', W')
        activations = self.activations
        weights = gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * activations).sum(dim=1, keepdim=True)  # (N,1,H',W')
        cam = F.relu(cam)

        cam = cam[0, 0].cpu().numpy()
        cam -= cam.min()
        if cam.max() > 0:
            cam /= cam.max()
        return cam


def overlay_heatmap_on_image(
    image_path: str, heatmap: np.ndarray, output_path: str, alpha: float = 0.5
) -> str:
    """
    Overlay a heatmap (H, W) in [0,1] over the original image and save it.
    """
    img = Image.open(image_path).convert("RGB")
    img_np = np.array(img)
    h, w = img_np.shape[:2]

    heatmap_resized = cv2.resize(heatmap, (w, h))
    heatmap_color = cv2.applyColorMap(
        (heatmap_resized * 255).astype(np.uint8), cv2.COLORMAP_JET
    )
    heatmap_color = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

    overlay = (alpha * heatmap_color + (1 - alpha) * img_np).astype(np.uint8)

    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(overlay).save(out_path)
    return str(out_path)

