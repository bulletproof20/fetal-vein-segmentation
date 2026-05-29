"""Dataset da pipeline de segmentação (lógica única)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
import numpy as np


@dataclass
class DatasetPaths:
    images_dir: Path
    masks_dir: Path
    extensions: tuple[str, ...]


def resolve_dataset_paths() -> DatasetPaths:
    """Lê caminhos definidos pelo runtime via variáveis de ambiente."""
    root = Path(os.environ.get("PROJECT_ROOT", ".")).resolve()
    dataset_root = Path(os.environ.get("FETAL_DATASET_PATH", root / "02_dataset")).resolve()
    images_dir = Path(os.environ.get("FETAL_IMAGES_DIR", dataset_root / "images")).resolve()
    masks_dir = Path(os.environ.get("FETAL_MASKS_DIR", dataset_root / "masks")).resolve()
    return DatasetPaths(
        images_dir=images_dir,
        masks_dir=masks_dir,
        extensions=(".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"),
    )


def list_paired_samples(paths: DatasetPaths) -> list[tuple[Path, Path]]:
    """Emparelha imagens e máscaras pelo nome de ficheiro (sem extensão)."""
    images: dict[str, Path] = {}
    masks: dict[str, Path] = {}

    for folder, store in ((paths.images_dir, images), (paths.masks_dir, masks)):
        if not folder.is_dir():
            continue
        for file_path in folder.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in paths.extensions:
                store[file_path.stem] = file_path

    pairs: list[tuple[Path, Path]] = []
    for stem, image_path in sorted(images.items()):
        mask_path = masks.get(stem)
        if mask_path is not None:
            pairs.append((image_path, mask_path))
    return pairs


def load_grayscale_array(path: Path) -> np.ndarray:
    """Carrega imagem em escala de cinzentos normalizada [0, 1]."""
    with Image.open(path) as img:
        array = np.asarray(img.convert("L"), dtype=np.float32)
    if array.max() > 1.0:
        array = array / 255.0
    return array
