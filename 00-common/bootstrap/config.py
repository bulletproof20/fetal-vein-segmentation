"""Configuração central do projeto fetal_vein_segmentation."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


def _detect_project_root() -> Path:
    """Deteta a raiz do repositório a partir de env ou estrutura de pastas."""
    env_root = os.environ.get("PROJECT_ROOT")
    if env_root:
        return Path(env_root).resolve()

    here = Path(__file__).resolve().parent
    candidates = [
        here.parent.parent,  # 00-common/bootstrap -> raiz
        Path.cwd(),
    ]
    for candidate in candidates:
        if (candidate / "00-common").is_dir() and (candidate / "10-docker").is_dir():
            return candidate.resolve()

    return here.parent.parent.resolve()


@dataclass
class ProjectConfig:
    """Caminhos e opções globais do projeto."""

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
    common_dir: Path = field(default_factory=Path)
    bootstrap_dir: Path = field(default_factory=Path)

    @property
    def required_directories(self) -> list[Path]:
        """Diretórios que o bootstrap deve garantir."""
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
            self.results_dir / "final-results",
            self.common_dir,
            self.bootstrap_dir,
        ]

    @property
    def dataset_image_extensions(self) -> tuple[str, ...]:
        return (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp")


def load_config() -> ProjectConfig:
    """Carrega configuração a partir do ambiente e da estrutura do projeto."""
    root = _detect_project_root()
    data_dir = Path(os.environ.get("DATA_DIR", root / "02-dataset")).resolve()

    return ProjectConfig(
        root=root,
        data_dir=data_dir,
        images_dir=Path(os.environ.get("IMAGES_DIR", data_dir / "images")).resolve(),
        masks_dir=Path(os.environ.get("MASKS_DIR", data_dir / "masks")).resolve(),
        preprocessing_output=Path(
            os.environ.get("PREPROCESSING_OUTPUT", root / "03-preprocessing" / "outputs")
        ).resolve(),
        segmentation_output=Path(
            os.environ.get("SEGMENTATION_OUTPUT", root / "04-segmentation" / "outputs")
        ).resolve(),
        postprocessing_output=Path(
            os.environ.get("POSTPROCESSING_OUTPUT", root / "05-postprocessing" / "outputs")
        ).resolve(),
        evaluation_dir=Path(
            os.environ.get("EVALUATION_DIR", root / "06-evaluation")
        ).resolve(),
        results_dir=Path(os.environ.get("RESULTS_DIR", root / "07-results")).resolve(),
        strict_mode=os.environ.get("BOOTSTRAP_STRICT", "1").strip().lower()
        in ("1", "true", "yes", "on"),
        jupyter_port=int(os.environ.get("JUPYTER_PORT", "8888")),
        common_dir=(root / "00-common").resolve(),
        bootstrap_dir=(root / "00-common" / "bootstrap").resolve(),
    )


def iter_common_notebooks(cfg: ProjectConfig) -> Iterable[Path]:
    """Notebooks da biblioteca 00-common."""
    names = [
        "01-functions.ipynb",
        "02-filters.ipynb",
        "03-morphology.ipynb",
        "04-metrics.ipynb",
        "05-visualization.ipynb",
        "06-uploading.ipynb",
    ]
    for name in names:
        yield cfg.common_dir / name
