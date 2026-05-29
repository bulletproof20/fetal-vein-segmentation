#!/usr/bin/env python3
"""Pipeline única de treino — executada em qualquer runtime."""

from __future__ import annotations

import json
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from dataset import DatasetPaths, list_paired_samples, load_grayscale_array, resolve_dataset_paths
from model import build_model


def _pipeline_config_path() -> Path:
    return Path(__file__).resolve().parent / "config.yaml"


def load_pipeline_config() -> dict:
    with _pipeline_config_path().open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def resolve_output_root() -> Path:
    output = Path(
        os.environ.get(
            "FETAL_OUTPUT_PATH",
            Path(__file__).resolve().parent / "outputs",
        )
    ).resolve()
    output.mkdir(parents=True, exist_ok=True)
    return output


def resolve_device() -> str:
    requested = os.environ.get("FETAL_DEVICE", "cpu").strip().lower()
    try:
        import torch
    except ImportError:
        return "cpu"

    if requested.startswith("cuda") and torch.cuda.is_available():
        return "cuda"
    return "cpu"


def prepare_runtime_if_needed(project_root: Path) -> None:
    """Prepara ambiente via adapter quando FETAL_PROVIDER não está definido."""
    if os.environ.get("FETAL_PROVIDER"):
        return

    provider = os.environ.get("BOOTSTRAP_PROFILE", "local_cpu").strip().lower()
    runtime = project_root / "99_system" / "01_runtime"
    adapter_map = {
        "local_cpu": runtime / "local_cpu" / "adapter.py",
        "local-cpu": runtime / "local_cpu" / "adapter.py",
        "cpu": runtime / "local_cpu" / "adapter.py",
        "local_gpu": runtime / "local_gpu" / "adapter.py",
        "local-gpu": runtime / "local_gpu" / "adapter.py",
        "gpu": runtime / "local_gpu" / "adapter.py",
        "kaggle": runtime / "kaggle" / "adapter.py",
    }
    adapter_path = adapter_map.get(provider)
    if adapter_path is None or not adapter_path.exists():
        return

    import importlib.util

    spec = importlib.util.spec_from_file_location("runtime_adapter", adapter_path)
    if spec is None or spec.loader is None:
        return
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "prepare_environment"):
        module.prepare_environment(project_root)


def train() -> int:
    project_root = Path(os.environ.get("PROJECT_ROOT", Path(__file__).resolve().parent.parent))
    prepare_runtime_if_needed(project_root)

    cfg = load_pipeline_config()
    paths = resolve_dataset_paths()
    pairs = list_paired_samples(paths)
    output_root = resolve_output_root()
    device_name = resolve_device()

    checkpoints_dir = output_root / cfg.get("outputs", {}).get("checkpoints_dir", "checkpoints")
    logs_dir = output_root / cfg.get("outputs", {}).get("logs_dir", "logs")
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    provider = os.environ.get("FETAL_PROVIDER", "unknown")
    print("=== fetal_vein_segmentation — train.py ===")
    print(f"provider      : {provider}")
    print(f"device        : {device_name}")
    print(f"dataset       : {paths.images_dir.parent}")
    print(f"output        : {output_root}")
    print(f"samples       : {len(pairs)}")

    if len(pairs) == 0:
        print("AVISO: nenhum par imagem/máscara encontrado. Treino em modo dry-run.")
        metrics = {
            "status": "dry_run",
            "reason": "dataset_empty",
            "provider": provider,
            "device": device_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        metrics_path = output_root / cfg.get("outputs", {}).get("metrics_file", "metrics.json")
        metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
        return 0

    try:
        import torch
        from torch.utils.data import DataLoader, Dataset
    except ImportError:
        print("ERRO: PyTorch em falta. Use runtime local-gpu, kaggle ou instale torch.")
        return 1

    training_cfg = cfg.get("training", {})
    epochs = int(training_cfg.get("epochs", 5))
    batch_size = int(training_cfg.get("batch_size", 2))
    lr = float(training_cfg.get("learning_rate", 1e-4))
    seed = int(training_cfg.get("seed", 42))

    random.seed(seed)
    torch.manual_seed(seed)

    class PairDataset(Dataset):
        def __init__(self, samples: list[tuple[Path, Path]]) -> None:
            self.samples = samples

        def __len__(self) -> int:
            return len(self.samples)

        def __getitem__(self, index: int):
            image_path, mask_path = self.samples[index]
            image = load_grayscale_array(image_path)
            mask = load_grayscale_array(mask_path)
            image_t = torch.from_numpy(image).unsqueeze(0)
            mask_t = torch.from_numpy(mask).unsqueeze(0)
            return image_t, mask_t

    split = float(cfg.get("data", {}).get("train_split", 0.8))
    split_index = max(1, int(len(pairs) * split))
    train_pairs = pairs[:split_index]
    val_pairs = pairs[split_index:] or pairs[:1]

    train_loader = DataLoader(PairDataset(train_pairs), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(PairDataset(val_pairs), batch_size=batch_size, shuffle=False)

    model = build_model(cfg)
    device = torch.device(device_name)
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = torch.nn.MSELoss()

    history: list[dict] = []
    for epoch in range(1, epochs + 1):
        model.train()
        train_loss = 0.0
        for images, masks in train_loader:
            images = images.to(device)
            masks = masks.to(device)
            optimizer.zero_grad()
            preds = model(images)
            loss = loss_fn(preds, masks)
            loss.backward()
            optimizer.step()
            train_loss += float(loss.item())

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for images, masks in val_loader:
                images = images.to(device)
                masks = masks.to(device)
                preds = model(images)
                val_loss += float(loss_fn(preds, masks).item())

        epoch_metrics = {
            "epoch": epoch,
            "train_loss": train_loss / max(len(train_loader), 1),
            "val_loss": val_loss / max(len(val_loader), 1),
        }
        history.append(epoch_metrics)
        print(
            f"epoch {epoch}/{epochs} — "
            f"train_loss={epoch_metrics['train_loss']:.6f} "
            f"val_loss={epoch_metrics['val_loss']:.6f}"
        )

    checkpoint_path = checkpoints_dir / "last.pt"
    torch.save(
        {
            "model_state": model.state_dict(),
            "config": cfg,
            "provider": provider,
            "device": device_name,
        },
        checkpoint_path,
    )

    metrics = {
        "status": "completed",
        "provider": provider,
        "device": device_name,
        "epochs": epochs,
        "train_samples": len(train_pairs),
        "val_samples": len(val_pairs),
        "checkpoint": str(checkpoint_path.relative_to(output_root)),
        "history": history,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    metrics_path = output_root / cfg.get("outputs", {}).get("metrics_file", "metrics.json")
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"Checkpoint guardado em: {checkpoint_path}")
    return 0


def main() -> int:
    return train()


if __name__ == "__main__":
    raise SystemExit(main())
