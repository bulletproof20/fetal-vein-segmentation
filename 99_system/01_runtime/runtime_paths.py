"""Shared utilities for runtime adapters (no training logic)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def detect_project_root() -> Path:
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).resolve()
    here = Path(__file__).resolve().parent
    candidate = here.parent.parent  # 99_system/01_runtime -> repo root
    if (candidate / "00_common").is_dir() and (candidate / "99_system" / "01_runtime").is_dir():
        return candidate
    return Path.cwd().resolve()


def load_runtime_yaml(config_path: Path) -> dict[str, Any]:
    """Load runtime YAML (PyYAML when available, otherwise a minimal parser)."""
    try:
        import yaml  # type: ignore

        with config_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except ImportError:
        data = {}
        for line in config_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or ":" not in stripped:
                continue
            key, value = stripped.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")

    if not isinstance(data, dict):
        raise ValueError(f"Invalid config.yaml: {config_path}")
    return data


@dataclass
class ResolvedRuntimePaths:
    provider: str
    project_root: Path
    dataset_path: Path
    output_path: Path
    images_dir: Path
    masks_dir: Path
    device: str
    config_path: Path


def resolve_paths(config_path: Path, project_root: Path | None = None) -> ResolvedRuntimePaths:
    """Resolve paths relative to the repository root."""
    root = project_root or detect_project_root()
    cfg = load_runtime_yaml(config_path)

    provider = str(cfg.get("provider", "local_cpu"))
    device = str(cfg.get("device", "cpu"))

    dataset_path = Path(cfg.get("dataset_path", "./02_dataset"))
    output_path = Path(cfg.get("output_path", "./04_segmentation/outputs"))

    if not dataset_path.is_absolute():
        dataset_path = (root / dataset_path).resolve()
    else:
        dataset_path = dataset_path.resolve()

    if not output_path.is_absolute():
        output_path = (root / output_path).resolve()
    else:
        output_path = output_path.resolve()

    images_dir = Path(cfg.get("images_dir", dataset_path / "images"))
    masks_dir = Path(cfg.get("masks_dir", dataset_path / "labels"))
    if not images_dir.is_absolute():
        images_dir = (root / images_dir).resolve()
    if not masks_dir.is_absolute():
        masks_dir = (root / masks_dir).resolve()
    if not masks_dir.is_dir():
        fallback = (dataset_path / "masks").resolve()
        if fallback.is_dir():
            masks_dir = fallback

    return ResolvedRuntimePaths(
        provider=provider,
        project_root=root,
        dataset_path=dataset_path,
        output_path=output_path,
        images_dir=images_dir,
        masks_dir=masks_dir,
        device=device,
        config_path=config_path.resolve(),
    )


def apply_runtime_env(paths: ResolvedRuntimePaths) -> None:
    """Publish environment variables consumed by the single training pipeline."""
    os.environ["FETAL_PROVIDER"] = paths.provider
    os.environ["FETAL_DATASET_PATH"] = str(paths.dataset_path)
    os.environ["FETAL_OUTPUT_PATH"] = str(paths.output_path)
    os.environ["FETAL_IMAGES_DIR"] = str(paths.images_dir)
    os.environ["FETAL_MASKS_DIR"] = str(paths.masks_dir)
    os.environ["FETAL_DEVICE"] = paths.device
    os.environ["PROJECT_ROOT"] = str(paths.project_root)
