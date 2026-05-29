"""Adapter de runtime: Kaggle Notebooks (GPU)."""

from __future__ import annotations

import os
import shutil
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
    root = project_root or _detect_kaggle_root()
    return resolve_paths(CONFIG_PATH, project_root=root)


def _detect_kaggle_root() -> Path:
    if Path("/kaggle/working").exists():
        for candidate in (Path("/kaggle/working"), Path.cwd()):
            if (candidate / "04_segmentation").exists() or (
                candidate / "99_system" / "01_runtime"
            ).exists():
                return candidate.resolve()
        return Path("/kaggle/working").resolve()
    return _PROJECT_ROOT


def prepare_environment(project_root: Path | None = None) -> ResolvedRuntimePaths:
    paths = resolve_paths_runtime(project_root)

    # No Kaggle, o dataset de input pode estar montado fora da raiz do repo
    if Path("/kaggle/input").exists() and not paths.dataset_path.exists():
        input_dirs = sorted(Path("/kaggle/input").iterdir())
        if input_dirs:
            paths.dataset_path = input_dirs[0].resolve()
            paths.images_dir = paths.dataset_path / "images"
            labels_dir = paths.dataset_path / "labels"
            masks_dir = paths.dataset_path / "masks"
            if labels_dir.is_dir():
                paths.masks_dir = labels_dir
            else:
                paths.masks_dir = masks_dir

    paths.output_path.mkdir(parents=True, exist_ok=True)
    apply_runtime_env(paths)
    os.environ["BOOTSTRAP_PROFILE"] = "kaggle"
    return paths


def validate_runtime(project_root: Path | None = None) -> list[str]:
    paths = resolve_paths_runtime(project_root)
    issues: list[str] = []

    if not Path("/kaggle").exists() and os.environ.get("FETAL_FORCE_KAGGLE") != "1":
        issues.append("Ambiente Kaggle não detetado (/kaggle ausente)")

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
        return False, "CUDA indisponível no kernel Kaggle"

    return True, f"CUDA Kaggle ({torch.cuda.get_device_name(0)})"


def sync_outputs(project_root: Path | None = None) -> Path:
    """Copia outputs da pipeline para /kaggle/working (download no Kaggle)."""
    paths = resolve_paths_runtime(project_root)
    working = Path("/kaggle/working")
    if not working.exists():
        return paths.output_path

    sync_target = working / "output"
    if sync_target.exists():
        shutil.rmtree(sync_target)
    shutil.copytree(paths.output_path, sync_target)
    return sync_target


if __name__ == "__main__":
    prepared = prepare_environment()
    problems = validate_runtime()
    print("Runtime kaggle preparado:")
    print(f"  provider={prepared.provider}")
    print(f"  dataset={prepared.dataset_path}")
    print(f"  output={prepared.output_path}")
    if problems:
        print("  avisos:")
        for item in problems:
            print(f"    - {item}")
