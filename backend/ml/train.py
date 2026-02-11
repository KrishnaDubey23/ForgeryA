"""
Training script for Aadhaar forgery detection using DenseNet121 and MobileNetV2.

Dataset structure (example):

data/
  train/
    authentic/
      img1.jpg
      ...
    forged/
      img2.jpg
      ...
  val/
    authentic/
      ...
    forged/
      ...

Labels:
  authentic -> 0
  forged    -> 1
"""

import os
from pathlib import Path
from typing import Tuple

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from .densenet import DenseNet121Binary
from .mobilenet import MobileNetV2Binary


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def build_dataloaders(
    data_dir: str, batch_size: int = 16
) -> Tuple[DataLoader, DataLoader]:
    train_dir = os.path.join(data_dir, "train")
    val_dir = os.path.join(data_dir, "val")

    transform_train = transforms.Compose(
        [
            transforms.Resize((384, 384)),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )

    transform_val = transforms.Compose(
        [
            transforms.Resize((384, 384)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )

    train_ds = datasets.ImageFolder(train_dir, transform=transform_train)
    val_ds = datasets.ImageFolder(val_dir, transform=transform_val)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=4)
    return train_loader, val_loader


def train_one_model(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    checkpoint_path: str,
    epochs: int = 5,
    lr: float = 1e-4,
) -> Tuple[float, float]:
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    best_val_acc = 0.0
    best_val_f1 = 0.0

    model.to(device)

    for epoch in range(epochs):
        model.train()
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.float().to(device)

            optimizer.zero_grad()
            logits = model(images)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()

        # Validation
        model.eval()
        tp = fp = fn = tn = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                labels = labels.float().to(device)
                logits = model(images)
                probs = torch.sigmoid(logits)
                preds = (probs > 0.5).float()

                tp += ((preds == 1) & (labels == 1)).sum().item()
                tn += ((preds == 0) & (labels == 0)).sum().item()
                fp += ((preds == 1) & (labels == 0)).sum().item()
                fn += ((preds == 0) & (labels == 1)).sum().item()

        total = tp + tn + fp + fn
        acc = (tp + tn) / total if total > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0
        )

        if acc > best_val_acc:
            best_val_acc = acc
            best_val_f1 = f1
            Path(checkpoint_path).parent.mkdir(parents=True, exist_ok=True)
            torch.save(model.state_dict(), checkpoint_path)

        print(
            f"Epoch {epoch+1}/{epochs} - acc={acc:.4f}, precision={precision:.4f}, recall={recall:.4f}, f1={f1:.4f}"
        )

    return best_val_acc, best_val_f1


def train_both_models(data_dir: str, checkpoint_dir: str, epochs: int = 5):
    train_loader, val_loader = build_dataloaders(data_dir)

    densenet = DenseNet121Binary(pretrained=True)
    dn_ckpt = os.path.join(checkpoint_dir, "densenet121_aadhaar.pt")
    dn_acc, dn_f1 = train_one_model(densenet, train_loader, val_loader, dn_ckpt, epochs=epochs)

    mobilenet = MobileNetV2Binary(pretrained=True)
    mb_ckpt = os.path.join(checkpoint_dir, "mobilenetv2_aadhaar.pt")
    mb_acc, mb_f1 = train_one_model(mobilenet, train_loader, val_loader, mb_ckpt, epochs=epochs)

    print("DenseNet best acc/f1:", dn_acc, dn_f1)
    print("MobileNet best acc/f1:", mb_acc, mb_f1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, required=True, help="Path to dataset root")
    parser.add_argument("--checkpoint_dir", type=str, default="ml/checkpoints")
    parser.add_argument("--epochs", type=int, default=5)
    args = parser.parse_args()

    train_both_models(args.data_dir, args.checkpoint_dir, epochs=args.epochs)

