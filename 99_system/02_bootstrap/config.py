"""Central configuration for the fetal_vein_segmentation project."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

PROFILE_ALIASES = {
    "cpu": "local_cpu",
    "gpu": "local_gpu",
    "local-cpu": "local_cpu",
    "local-gpu": "local_gpu",
}
VALID_PROFILES = frozenset(
    {"local_cpu", "local_gpu", "kaggle", "cpu", "gpu", "local-cpu", "local-gpu"}
)


def normalize_profile(raw: str) -> str:
    """Normalize runtime profile (accepts cpu/gpu aliases)."""
    profile = raw.strip().lower()
    return PROFILE_ALIASES.get(profile, profile)


def is_gpu_profile(profile: str) -> bool:
    """Return True when the profile requires a GPU stack (PyTorch/CUDA/MONAI)."""
    normalized = normalize_profile(profile)
    return normalized in ("local_gpu", "kaggle")


def _detect_project_root() -> Path:
    """Detect repository root from env or folder markers."""
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).resolve()

    here = Path(__file__).resolve().parent
    candidates = [
        here.parent.parent,  # 99_system/02_bootstrap -> repo root
        Path.cwd(),
    ]
    for candidate in candidates:
        if (candidate / "00_common").is_dir() and (candidate / "99_system" / "01_runtime").is_dir():
            return candidate.resolve()

    return here.parent.parent.resolve()


@dataclass
class ProjectConfig:
    """Global project paths and options."""

    root: Path
    data_dir: Path
    images_dir: Path
    masks_dir: Path
    preprocessing_output: Path
    segmentation_output: Path
    postprocessing_output: Path
    evaluation_dir: Path
    results_dir: Path
    strict_mode: bool = True
    jupyter_port: int = 8888
    profile: str = "local_cpu"
    common_dir: Path = field(default_factory=Path)
    bootstrap_dir: Path = field(default_factory=Path)
    runtime_dir: Path = field(default_factory=Path)
    system_dir: Path = field(default_factory=Path)

    @property
    def normalized_profile(self) -> str:
        return normalize_profile(self.profile)

    @property
    def requires_gpu_stack(self) -> bool:
        return is_gpu_profile(self.profile)

    @property
    def runtime_adapter_dir(self) -> Path:
        mapping = {
            "local_cpu": self.runtime_dir / "local_cpu",
            "local_gpu": self.runtime_dir / "local_gpu",
            "kaggle": self.runtime_dir / "kaggle",
        }
        return mapping.get(self.normalized_profile, mapping["local_cpu"])

    @property
    def required_directories(self) -> list[Path]:
        """Directories the bootstrap must ensure exist."""
        return [
            self.data_dir,
            self.images_dir,
            self.masks_dir,
            self.data_dir / "statistics",
            self.data_dir / "figures",
            self.preprocessing_output,
            self.segmentation_output,
            self.postprocessing_output,
            self.evaluation_dir,
            self.evaluation_dir / "metrics",
            self.evaluation_dir / "tables",
            self.evaluation_dir / "plots",
            self.results_dir,
            self.results_dir / "figures",
            self.results_dir / "comparisons",
            self.results_dir / "reports",
            self.common_dir,
            self.bootstrap_dir,
        ]

    @property
    def dataset_image_extensions(self) -> tuple[str, ...]:
        return (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp")


def load_config() -> ProjectConfig:
    """Load configuration from environment and repository layout."""
    root = _detect_project_root()
    system_dir = (root / "99_system").resolve()
    data_dir = Path(os.environ.get("DATA_DIR", root / "02_dataset")).resolve()

    profile = os.environ.get("BOOTSTRAP_PROFILE", "local_cpu").strip().lower()
    if profile not in VALID_PROFILES:
        profile = "local_cpu"

    strict_env = os.environ.get("BOOTSTRAP_STRICT")
    if strict_env is None:
        strict_mode = is_gpu_profile(profile)
    else:
        strict_mode = strict_env.strip().lower() in ("1", "true", "yes", "on")

    runtime_dir = Path(
        os.environ.get("RUNTIME_DIR", system_dir / "01_runtime")
    ).resolve()

    return ProjectConfig(
        root=root,
        data_dir=data_dir,
        images_dir=Path(os.environ.get("IMAGES_DIR", data_dir / "images")).resolve(),
        masks_dir=Path(
            os.environ.get(
                "MASKS_DIR",
                data_dir / "labels" if (data_dir / "labels").is_dir() else data_dir / "masks",
            )
        ).resolve(),
        preprocessing_output=Path(
            os.environ.get("PREPROCESSING_OUTPUT", root / "03_preprocessing" / "outputs")
        ).resolve(),
        segmentation_output=Path(
            os.environ.get("SEGMENTATION_OUTPUT", root / "04_segmentation" / "outputs")
        ).resolve(),
        postprocessing_output=Path(
            os.environ.get("POSTPROCESSING_OUTPUT", root / "05_postprocessing" / "outputs")
        ).resolve(),
        evaluation_dir=Path(
            os.environ.get("EVALUATION_DIR", root / "06_evaluation")
        ).resolve(),
        results_dir=Path(os.environ.get("RESULTS_DIR", root / "07_results")).resolve(),
        strict_mode=strict_mode,
        jupyter_port=int(os.environ.get("JUPYTER_PORT", "8888")),
        profile=profile,
        common_dir=(root / "00_common").resolve(),
        bootstrap_dir=(system_dir / "02_bootstrap").resolve(),
        runtime_dir=runtime_dir,
        system_dir=system_dir,
    )


def iter_common_notebooks(cfg: ProjectConfig) -> Iterable[Path]:
    """Notebooks in the shared 00_common library."""
    names = [
        "01_functions.ipynb",
        "02_filters.ipynb",
        "03_morphology.ipynb",
        "04_metrics.ipynb",
        "05_visualization.ipynb",
        "06_uploading.ipynb",
        "07_training_provider.ipynb",
    ]
    for name in names:
        yield cfg.common_dir / name
