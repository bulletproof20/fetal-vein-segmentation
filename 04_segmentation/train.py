#!/usr/bin/env python3
"""Pipeline única de treino — executada em qualquer runtime."""

from __future__ import annotations

import csv
import json
import logging
import os
import random
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from dataset import (
    DatasetSplit,
    load_image_array,
    load_label_array,
    list_paired_samples,
    resolve_dataset_paths,
    split_pairs,
)
from model import build_model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


@dataclass
class EpochResult:
    epoch: int
    train_loss: float
    val_loss: float
    val_dice: float


def _pipeline_config_path() -> Path:
    return Path(__file__).resolve().parent / "config.yaml"


def load_pipeline_config() -> dict[str, Any]:
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


def resolve_project_root() -> Path:
    return Path(os.environ.get("PROJECT_ROOT", Path(__file__).resolve().parent.parent)).resolve()


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


def setup_reproducibility(cfg: dict[str, Any]) -> int:
    """Seeds globais + MONAI set_determinism para execuções reproduzíveis."""
    seed = int(cfg.get("training", {}).get("seed", 0))
    random.seed(seed)
    np.random.seed(seed)

    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass

    try:
        from monai.utils import set_determinism

        set_determinism(seed=seed)
        logger.info("Reprodutibilidade: seed=%s (MONAI set_determinism)", seed)
    except ImportError:
        logger.warning("MONAI indisponível para set_determinism; apenas seeds Python/PyTorch")

    return seed


def build_loss_function(cfg: dict[str, Any]):
    """DiceLoss MONAI — adequado a segmentação binária com sigmoid na loss."""
    from monai.losses import DiceLoss

    loss_cfg = cfg.get("loss", {})
    return DiceLoss(
        smooth_nr=float(loss_cfg.get("smooth_nr", 0)),
        smooth_dr=float(loss_cfg.get("smooth_dr", 1e-5)),
        squared_pred=bool(loss_cfg.get("squared_pred", True)),
        to_onehot_y=bool(loss_cfg.get("to_onehot_y", False)),
        sigmoid=bool(loss_cfg.get("sigmoid", True)),
    )


def build_dice_metric(cfg: dict[str, Any]):
    from monai.metrics import DiceMetric

    metrics_cfg = cfg.get("metrics", {})
    return DiceMetric(
        include_background=bool(metrics_cfg.get("include_background", True)),
        reduction="mean",
    )


def build_scheduler(optimizer, cfg: dict[str, Any]):
    import torch

    sched_cfg = cfg.get("scheduler", {})
    name = str(sched_cfg.get("name", "cosine")).lower()
    epochs = int(cfg.get("training", {}).get("epochs", 150))
    if name == "cosine":
        t_max = int(sched_cfg.get("t_max", epochs))
        return torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=t_max)
    return None


def _prediction_mask(outputs, threshold: float):
    import torch

    probs = torch.sigmoid(outputs)
    return (probs > threshold).float()


def train_epoch(
    model,
    loader,
    loss_fn,
    optimizer,
    device,
) -> float:
    import torch

    model.train()
    total_loss = 0.0
    steps = 0
    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)
        optimizer.zero_grad(set_to_none=True)
        outputs = model(images)
        loss = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += float(loss.item())
        steps += 1
    return total_loss / max(steps, 1)


def validate(
    model,
    loader,
    loss_fn,
    dice_metric,
    device,
    threshold: float,
) -> tuple[float, float]:
    import torch

    model.eval()
    dice_metric.reset()
    total_loss = 0.0
    steps = 0

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            total_loss += float(loss_fn(outputs, labels).item())
            steps += 1
            preds = _prediction_mask(outputs, threshold)
            dice_metric(y_pred=preds, y=labels)

    mean_dice = float(dice_metric.aggregate().item()) if steps > 0 else 0.0
    dice_metric.reset()
    mean_loss = total_loss / max(steps, 1)
    return mean_loss, mean_dice


def run_test(
    model,
    loader,
    loss_fn,
    dice_metric,
    device,
    threshold: float,
) -> dict[str, float]:
    import torch

    model.eval()
    dice_metric.reset()
    total_loss = 0.0
    steps = 0

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs = model(images)
            total_loss += float(loss_fn(outputs, labels).item())
            steps += 1
            preds = _prediction_mask(outputs, threshold)
            dice_metric(y_pred=preds, y=labels)

    return {
        "test_loss": total_loss / max(steps, 1),
        "test_dice": float(dice_metric.aggregate().item()) if steps > 0 else 0.0,
        "test_samples": steps * loader.batch_size if hasattr(loader, "batch_size") else steps,
    }


def save_checkpoint(
    path: Path,
    *,
    model,
    optimizer,
    scheduler,
    epoch: int,
    best_val_dice: float,
    cfg: dict[str, Any],
    extra: dict[str, Any] | None = None,
) -> None:
    import torch

    payload: dict[str, Any] = {
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "best_val_dice": best_val_dice,
        "config": cfg,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    if scheduler is not None:
        payload["scheduler_state_dict"] = scheduler.state_dict()
    if extra:
        payload.update(extra)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(payload, path)
    logger.info("Checkpoint guardado: %s", path)


def load_checkpoint(path: Path, model, optimizer=None, scheduler=None, device=None) -> dict[str, Any]:
    import torch

    map_location = device if device is not None else "cpu"
    data = torch.load(path, map_location=map_location, weights_only=False)
    model.load_state_dict(data["model_state_dict"])
    if optimizer is not None and "optimizer_state_dict" in data:
        optimizer.load_state_dict(data["optimizer_state_dict"])
    if scheduler is not None and "scheduler_state_dict" in data:
        scheduler.load_state_dict(data["scheduler_state_dict"])
    return data


def export_predictions(
    model,
    samples: list[tuple[Path, Path]],
    output_dir: Path,
    device,
    threshold: float,
) -> int:
    import torch
    from PIL import Image

    output_dir.mkdir(parents=True, exist_ok=True)
    model.eval()
    count = 0

    with torch.no_grad():
        for image_path, _label_path in samples:
            image = load_image_array(image_path)
            tensor = torch.from_numpy(image).unsqueeze(0).unsqueeze(0).to(device)
            outputs = model(tensor)
            mask = _prediction_mask(outputs, threshold)[0, 0].cpu().numpy()
            binary = (mask * 255).astype(np.uint8)
            out_path = output_dir / f"{image_path.stem}.png"
            Image.fromarray(binary, mode="L").save(out_path)
            count += 1

    logger.info("Exportadas %d máscaras para %s", count, output_dir)
    return count


def persist_evaluation_artifacts(
    project_root: Path,
    output_root: Path,
    cfg: dict[str, Any],
    history: list[EpochResult],
    test_metrics: dict[str, float],
    split: DatasetSplit,
    provider: str,
    device_name: str,
    best_val_dice: float,
    best_epoch: int,
) -> Path:
    eval_cfg = cfg.get("evaluation", {})
    eval_root = project_root / "06_evaluation"
    metrics_dir = eval_root / eval_cfg.get("metrics_subdir", "metrics")
    plots_dir = eval_root / eval_cfg.get("plots_subdir", "plots")
    tables_dir = eval_root / eval_cfg.get("tables_subdir", "tables")
    for directory in (metrics_dir, plots_dir, tables_dir):
        directory.mkdir(parents=True, exist_ok=True)

    summary = {
        "status": "completed",
        "provider": provider,
        "device": device_name,
        "best_val_dice": best_val_dice,
        "best_epoch": best_epoch,
        "test": test_metrics,
        "split_sizes": {
            "train": len(split.train),
            "val": len(split.val),
            "test": len(split.test),
        },
        "history": [
            {
                "epoch": h.epoch,
                "train_loss": h.train_loss,
                "val_loss": h.val_loss,
                "val_dice": h.val_dice,
            }
            for h in history
        ],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    summary_path = metrics_dir / "training_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    table_path = tables_dir / "split_summary.csv"
    with table_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["split", "count"])
        writer.writerow(["train", len(split.train)])
        writer.writerow(["val", len(split.val)])
        writer.writerow(["test", len(split.test)])

    try:
        import matplotlib.pyplot as plt

        epochs = [h.epoch for h in history]
        train_losses = [h.train_loss for h in history]
        val_losses = [h.val_loss for h in history]
        val_dices = [h.val_dice for h in history]

        fig, axes = plt.subplots(1, 3, figsize=(14, 4))
        axes[0].plot(epochs, train_losses, color="tab:red")
        axes[0].set_title("Train loss (Dice)")
        axes[0].set_xlabel("epoch")

        axes[1].plot(epochs, val_losses, color="tab:orange")
        axes[1].set_title("Validation loss (Dice)")
        axes[1].set_xlabel("epoch")

        axes[2].plot(epochs, val_dices, color="tab:green")
        axes[2].set_title("Validation Dice")
        axes[2].set_xlabel("epoch")

        fig.tight_layout()
        plot_path = plots_dir / "training_curves.png"
        fig.savefig(plot_path, dpi=120)
        plt.close(fig)
        logger.info("Curvas guardadas em %s", plot_path)
    except ImportError:
        logger.warning("matplotlib indisponível — curvas não geradas")

    results_dir = project_root / "07_results" / "metrics"
    results_dir.mkdir(parents=True, exist_ok=True)
    shutil_copy = summary_path.read_text(encoding="utf-8")
    (results_dir / "latest_training_summary.json").write_text(shutil_copy, encoding="utf-8")

    metrics_file = output_root / cfg.get("outputs", {}).get("metrics_file", "metrics.json")
    metrics_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    return summary_path


def train() -> int:
    project_root = resolve_project_root()
    prepare_runtime_if_needed(project_root)

    cfg = load_pipeline_config()
    setup_reproducibility(cfg)

    paths = resolve_dataset_paths(cfg)
    pairs = list_paired_samples(paths)
    output_root = resolve_output_root()
    device_name = resolve_device()

    outputs_cfg = cfg.get("outputs", {})
    checkpoints_dir = output_root / outputs_cfg.get("checkpoints_dir", "checkpoints")
    predictions_dir = output_root / outputs_cfg.get("predictions_dir", "predictions")
    logs_dir = output_root / outputs_cfg.get("logs_dir", "logs")
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    provider = os.environ.get("FETAL_PROVIDER", "unknown")
    min_required = int(cfg.get("training", {}).get("min_samples_required", 3))

    logger.info("=== fetal_vein_segmentation — train.py ===")
    logger.info("provider       : %s", provider)
    logger.info("device         : %s", device_name)
    logger.info("dataset root   : %s", paths.images_dir.parent)
    logger.info("images dir     : %s", paths.images_dir)
    logger.info("ground truth   : %s (%s)", paths.ground_truth_dir, paths.ground_truth_source)
    logger.info("output root    : %s", output_root)
    logger.info("paired samples : %d", len(pairs))

    if len(pairs) < min_required:
        logger.error(
            "Dataset insuficiente: %d pares (mínimo %d). "
            "Verifique images/ e labels/ (ou FETAL_MASKS_DIR).",
            len(pairs),
            min_required,
        )
        return 1

    try:
        import torch
        from torch.utils.data import DataLoader, Dataset
    except ImportError:
        logger.error("PyTorch em falta. Use runtime local_gpu, kaggle ou instale torch.")
        return 1

    try:
        loss_fn = build_loss_function(cfg)
        dice_metric = build_dice_metric(cfg)
    except ImportError:
        logger.error("MONAI em falta. Instale monai>=1.5 para DiceLoss/DiceMetric.")
        return 1

    training_cfg = cfg.get("training", {})
    metrics_cfg = cfg.get("metrics", {})
    threshold = float(metrics_cfg.get("threshold", 0.5))
    label_threshold = float(cfg.get("data", {}).get("label_binarization_threshold", threshold))

    epochs = int(training_cfg.get("epochs", 150))
    val_interval = int(training_cfg.get("val_interval", 1))
    lr = float(training_cfg.get("learning_rate", 0.01))
    num_workers = int(training_cfg.get("num_workers", 0))
    batch_train = int(training_cfg.get("batch_size_train", 10))
    batch_val = int(training_cfg.get("batch_size_val", 5))
    batch_test = int(training_cfg.get("batch_size_test", 1))

    split = split_pairs(pairs, cfg)
    if len(split.train) == 0 or len(split.val) == 0:
        logger.error("Split inválido: train=%d val=%d", len(split.train), len(split.val))
        return 1

    class PairDataset(Dataset):
        def __init__(self, samples: list[tuple[Path, Path]]) -> None:
            self.samples = samples

        def __len__(self) -> int:
            return len(self.samples)

        def __getitem__(self, index: int):
            image_path, label_path = self.samples[index]
            image = load_image_array(image_path)
            label = load_label_array(label_path, threshold=label_threshold)
            image_t = torch.from_numpy(image).unsqueeze(0)
            label_t = torch.from_numpy(label).unsqueeze(0)
            return image_t, label_t, image_path.name

    def collate_with_names(batch):
        images = torch.stack([b[0] for b in batch])
        labels = torch.stack([b[1] for b in batch])
        names = [b[2] for b in batch]
        return images, labels, names

    train_loader = DataLoader(
        PairDataset(split.train),
        batch_size=batch_train,
        shuffle=True,
        num_workers=num_workers,
        collate_fn=collate_with_names,
    )
    val_loader = DataLoader(
        PairDataset(split.val),
        batch_size=batch_val,
        shuffle=False,
        num_workers=num_workers,
        collate_fn=collate_with_names,
    )
    test_loader = DataLoader(
        PairDataset(split.test),
        batch_size=batch_test,
        shuffle=False,
        num_workers=num_workers,
        collate_fn=collate_with_names,
    ) if split.test else None

    model = build_model(cfg)
    device = torch.device(device_name)
    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = build_scheduler(optimizer, cfg)

    best_val_dice = -1.0
    best_epoch = 0
    history: list[EpochResult] = []

    for epoch in range(1, epochs + 1):
        train_loss = train_epoch(model, train_loader, loss_fn, optimizer, device)
        val_loss, val_dice = 0.0, 0.0

        if epoch % val_interval == 0:
            val_loss, val_dice = validate(
                model, val_loader, loss_fn, dice_metric, device, threshold
            )

            if val_dice > best_val_dice:
                best_val_dice = val_dice
                best_epoch = epoch
                save_checkpoint(
                    checkpoints_dir / "best.pt",
                    model=model,
                    optimizer=optimizer,
                    scheduler=scheduler,
                    epoch=epoch,
                    best_val_dice=best_val_dice,
                    cfg=cfg,
                    extra={"provider": provider, "device": device_name, "kind": "best"},
                )

        if scheduler is not None:
            scheduler.step()

        history.append(
            EpochResult(
                epoch=epoch,
                train_loss=train_loss,
                val_loss=val_loss,
                val_dice=val_dice,
            )
        )
        logger.info(
            "epoch %d/%d — train_loss=%.4f val_loss=%.4f val_dice=%.4f (best=%.4f @ ep%d)",
            epoch,
            epochs,
            train_loss,
            val_loss,
            val_dice,
            best_val_dice,
            best_epoch,
        )

    save_checkpoint(
        checkpoints_dir / "last.pt",
        model=model,
        optimizer=optimizer,
        scheduler=scheduler,
        epoch=epochs,
        best_val_dice=best_val_dice,
        cfg=cfg,
        extra={"provider": provider, "device": device_name, "kind": "last"},
    )

    test_metrics: dict[str, float] = {"test_loss": 0.0, "test_dice": 0.0, "test_samples": 0}
    if test_loader is not None and len(split.test) > 0:
        best_path = checkpoints_dir / "best.pt"
        if best_path.exists():
            load_checkpoint(best_path, model, device=device)
            logger.info("Teste: carregado best.pt (época %d, dice=%.4f)", best_epoch, best_val_dice)
        test_metrics = run_test(model, test_loader, loss_fn, build_dice_metric(cfg), device, threshold)
        test_metrics["test_samples"] = len(split.test)
        logger.info(
            "Teste — loss=%.4f dice=%.4f (n=%d)",
            test_metrics["test_loss"],
            test_metrics["test_dice"],
            test_metrics["test_samples"],
        )
        export_predictions(model, split.test, predictions_dir, device, threshold)
    else:
        logger.warning("Conjunto de teste vazio — inferência/export ignoradas")

    persist_evaluation_artifacts(
        project_root,
        output_root,
        cfg,
        history,
        test_metrics,
        split,
        provider,
        device_name,
        best_val_dice,
        best_epoch,
    )

    logger.info("Treino concluído. Checkpoints em %s", checkpoints_dir)
    return 0


def main() -> int:
    return train()


if __name__ == "__main__":
    raise SystemExit(main())
