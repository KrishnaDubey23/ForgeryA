from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
from torchvision import models


class MobileNetV2Binary(nn.Module):
    def __init__(self, pretrained: bool = True):
        super().__init__()
        self.model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1 if pretrained else None)
        num_features = self.model.classifier[1].in_features
        self.model.classifier[1] = nn.Linear(num_features, 1)

    def forward(self, x):
        return self.model(x).squeeze(1)


def load_mobilenet_checkpoint(
    checkpoint_dir: str, device: Optional[torch.device] = None
) -> MobileNetV2Binary:
    device = device or torch.device("cpu")
    model = MobileNetV2Binary(pretrained=True)
    ckpt_path = Path(checkpoint_dir) / "mobilenetv2_aadhaar.pt"
    if ckpt_path.exists():
        state = torch.load(ckpt_path, map_location=device)
        model.load_state_dict(state)
    model.to(device)
    model.eval()
    return model

