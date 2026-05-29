"""Dataset da pipeline de segmentação (lógica única)."""

from __future__ import annotations

import logging
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)


@dataclass
class DatasetPaths:
    """Caminhos resolvidos para imagens e ground truth (máscaras binárias)."""

    images_dir: Path
    ground_truth_dir: Path
    extensions: tuple[str, ...]
    ground_truth_source: str


@dataclass
class DatasetSplit:
    """Partição reproduzível train / validation / test."""

    train: list[tuple[Path, Path]]
    val: list[tuple[Path, Path]]
    test: list[tuple[Path, Path]]


def resolve_ground_truth_dir(
    dataset_root: Path,
    primary_name: str = "labels",
    fallback_name: str = "masks",
) -> tuple[Path, str]:
    """Resolve diretório de GT: `labels/` é oficial; `masks/` é fallback legado."""
    primary = dataset_root / primary_name
    fallback = dataset_root / fallback_name

    if primary.is_dir() and any(primary.rglob("*")):
        logger.info("Ground truth: usando pasta oficial '%s' em %s", primary_name, primary)
        return primary.resolve(), primary_name

    if fallback.is_dir() and any(fallback.rglob("*")):
        logger.warning(
            "Ground truth: '%s' ausente ou vazia; fallback para '%s' em %s",
            primary_name,
            fallback_name,
            fallback,
        )
        return fallback.resolve(), fallback_name

    if primary.is_dir():
        return primary.resolve(), primary_name
    if fallback.is_dir():
        return fallback.resolve(), fallback_name

    logger.error(
        "Ground truth não encontrado em %s nem %s (dataset_root=%s)",
        primary,
        fallback,
        dataset_root,
    )
    return primary.resolve(), primary_name


def resolve_dataset_paths(cfg: dict[str, Any] | None = None) -> DatasetPaths:
    """Lê caminhos a partir do runtime (env) e configuração da pipeline."""
    cfg = cfg or {}
    data_cfg = cfg.get("data", {})

    root = Path(os.environ.get("PROJECT_ROOT", ".")).resolve()
    dataset_root = Path(os.environ.get("FETAL_DATASET_PATH", root / "02_dataset")).resolve()
    images_dir = Path(os.environ.get("FETAL_IMAGES_DIR", dataset_root / "images")).resolve()

    if os.environ.get("FETAL_MASKS_DIR"):
        gt_dir = Path(os.environ["FETAL_MASKS_DIR"]).resolve()
        source = gt_dir.name
        logger.info("Ground truth: FETAL_MASKS_DIR=%s", gt_dir)
    else:
        gt_dir, source = resolve_ground_truth_dir(
            dataset_root,
            str(data_cfg.get("primary_ground_truth_dir", "labels")),
            str(data_cfg.get("fallback_ground_truth_dir", "masks")),
        )

    extensions = tuple(data_cfg.get("image_extensions", [".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"]))

    return DatasetPaths(
        images_dir=images_dir,
        ground_truth_dir=gt_dir,
        extensions=tuple(ext.lower() for ext in extensions),
        ground_truth_source=source,
    )


def list_paired_samples(paths: DatasetPaths) -> list[tuple[Path, Path]]:
    """Emparelha imagens e ground truth pelo stem do ficheiro."""
    images: dict[str, Path] = {}
    labels: dict[str, Path] = {}

    if not paths.images_dir.is_dir():
        logger.error("Pasta de imagens em falta: %s", paths.images_dir)
        return []

    for file_path in paths.images_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in paths.extensions:
            images[file_path.stem] = file_path

    if paths.ground_truth_dir.is_dir():
        for file_path in paths.ground_truth_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in paths.extensions:
                labels[file_path.stem] = file_path
    else:
        logger.error("Pasta de ground truth em falta: %s", paths.ground_truth_dir)

    pairs: list[tuple[Path, Path]] = []
    missing_gt = []
    for stem, image_path in sorted(images.items()):
        label_path = labels.get(stem)
        if label_path is not None:
            pairs.append((image_path, label_path))
        else:
            missing_gt.append(stem)

    logger.info(
        "Dataset: %d imagens, %d GT, %d pares válidos, %d imagens sem GT",
        len(images),
        len(labels),
        len(pairs),
        len(missing_gt),
    )
    if missing_gt[:5]:
        logger.warning("Exemplos sem GT: %s", ", ".join(missing_gt[:5]))

    return pairs


def load_image_array(path: Path) -> np.ndarray:
    """Carrega imagem em escala de cinzentos normalizada para [0, 1]."""
    with Image.open(path) as img:
        array = np.asarray(img.convert("L"), dtype=np.float32)
    if array.max() > 1.0:
        array = array / 255.0
    return np.clip(array, 0.0, 1.0)


def load_label_array(path: Path, threshold: float = 0.5) -> np.ndarray:
    """Carrega máscara binária {0, 1} — sem normalização contínua da GT."""
    with Image.open(path) as img:
        array = np.asarray(img.convert("L"), dtype=np.float32)
    if array.max() > 1.0:
        array = array / 255.0
    binary = (array > threshold).astype(np.float32)
    return binary


def split_pairs(pairs: list[tuple[Path, Path]], cfg: dict[str, Any]) -> DatasetSplit:
    """Partição train/val/test reproduzível (counts ou ratios via YAML)."""
    data_cfg = cfg.get("data", {})
    split_cfg = data_cfg.get("split", {})
    seed = int(split_cfg.get("seed", data_cfg.get("seed", cfg.get("training", {}).get("seed", 0))))
    shuffle = bool(split_cfg.get("shuffle", True))
    mode = str(data_cfg.get("split_mode", split_cfg.get("mode", "counts"))).lower()

    ordered = list(pairs)
    if shuffle:
        rng = random.Random(seed)
        rng.shuffle(ordered)

    n = len(ordered)
    if n == 0:
        return DatasetSplit(train=[], val=[], test=[])

    train_count = data_cfg.get("train_count")
    val_count = data_cfg.get("val_count")
    test_count = data_cfg.get("test_count")

    if mode == "ratios" or (train_count is None and val_count is None):
        train_ratio = float(data_cfg.get("train_ratio", 0.7))
        val_ratio = float(data_cfg.get("val_ratio", 0.15))
        test_ratio = data_cfg.get("test_ratio")
        n_train = max(1, int(n * train_ratio))
        n_val = max(1, int(n * val_ratio))
        if test_ratio is not None:
            n_test = max(0, int(n * float(test_ratio)))
        else:
            n_test = max(0, n - n_train - n_val)
        if n_train + n_val + n_test > n:
            n_test = max(0, n - n_train - n_val)
    else:
        n_train = int(train_count) if train_count is not None else max(1, int(n * 0.7))
        n_val = int(val_count) if val_count is not None else max(1, int(n * 0.15))
        if test_count is not None:
            n_test = int(test_count)
        else:
            n_test = max(0, n - n_train - n_val)

    if n_train + n_val >= n:
        n_train = max(1, n - 2)
        n_val = 1
        n_test = max(0, n - n_train - n_val)
    elif n_train + n_val + n_test > n:
        n_test = max(0, n - n_train - n_val)

    train = ordered[:n_train]
    val = ordered[n_train : n_train + n_val]
    test = ordered[n_train + n_val : n_train + n_val + n_test]

    logger.info(
        "Split (%s, seed=%s): train=%d, val=%d, test=%d (total=%d)",
        mode,
        seed,
        len(train),
        len(val),
        len(test),
        n,
    )
    return DatasetSplit(train=train, val=val, test=test)


# Compatibilidade com imports legados
def load_grayscale_array(path: Path) -> np.ndarray:
    """Alias legado — preferir load_image_array para imagens."""
    return load_image_array(path)


@dataclass
class DatasetPathsLegacy:
    images_dir: Path
    masks_dir: Path
    extensions: tuple[str, ...]


def resolve_dataset_paths_legacy() -> DatasetPathsLegacy:
    paths = resolve_dataset_paths()
    return DatasetPathsLegacy(
        images_dir=paths.images_dir,
        masks_dir=paths.ground_truth_dir,
        extensions=paths.extensions,
    )
