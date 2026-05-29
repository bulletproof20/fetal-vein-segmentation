"""Adapter de runtime: desenvolvimento local com GPU/CUDA."""

from __future__ import annotations

import sys
from pathlib import Path

_RUNTIME_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _RUNTIME_DIR.parent.parent.parent
_RUNTIME_LIB = _PROJECT_ROOT / "99_system" / "01_runtime"
if str(_RUNTIME_LIB) not in sys.path:
    sys.path.insert(0, str(_RUNTIME_LIB))

from runtime_paths import ResolvedRuntimePaths, apply_runtime_env, resolve_paths  # noqa: E402

CONFIG_PATH = _RUNTIME_DIR / "config.yaml"


def resolve_paths_runtime(project_root: Path | None = None) -> ResolvedRuntimePaths:
    return resolve_paths(CONFIG_PATH, project_root=project_root)


def prepare_environment(project_root: Path | None = None) -> ResolvedRuntimePaths:
    paths = resolve_paths_runtime(project_root)
    paths.output_path.mkdir(parents=True, exist_ok=True)
    apply_runtime_env(paths)
    return paths


def validate_runtime(project_root: Path | None = None) -> list[str]:
    paths = resolve_paths_runtime(project_root)
    issues: list[str] = []

    if not paths.images_dir.exists():
        issues.append(f"Pasta de imagens em falta: {paths.images_dir}")
    if not paths.masks_dir.exists():
        issues.append(f"Pasta de máscaras em falta: {paths.masks_dir}")

    train_script = paths.project_root / "04_segmentation" / "train.py"
    if not train_script.exists():
        issues.append("Pipeline em falta: 04_segmentation/train.py")

    ok_cuda, msg_cuda = check_cuda()
    if not ok_cuda:
        issues.append(msg_cuda)

    return issues


def check_cuda() -> tuple[bool, str]:
    try:
        import torch
    except ImportError as exc:
        return False, f"PyTorch indisponível: {exc}"

    if not torch.cuda.is_available():
        return False, "CUDA indisponível — runtime local-gpu requer GPU"

    return True, f"CUDA disponível ({torch.cuda.get_device_name(0)})"


if __name__ == "__main__":
    prepared = prepare_environment()
    ok, msg = check_cuda()
    print("Runtime local-gpu preparado:")
    print(f"  provider={prepared.provider}")
    print(f"  dataset={prepared.dataset_path}")
    print(f"  output={prepared.output_path}")
    print(f"  device={prepared.device}")
    print(f"  cuda={msg} (ok={ok})")
