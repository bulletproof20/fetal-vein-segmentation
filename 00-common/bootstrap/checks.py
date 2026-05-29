"""Verificações de ambiente e estrutura do projeto."""

from __future__ import annotations

import importlib
import os
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Iterable

from config import ProjectConfig, iter_common_notebooks


class Level(str, Enum):
    OK = "OK"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class CheckResult:
    level: Level
    message: str
    name: str = ""


@dataclass
class CheckReport:
    results: list[CheckResult] = field(default_factory=list)

    def add(self, level: Level, message: str, name: str = "") -> None:
        self.results.append(CheckResult(level=level, message=message, name=name))
        prefix = f"[{level.value}]"
        print(f"{prefix} {message}")

    @property
    def has_fail(self) -> bool:
        return any(r.level == Level.FAIL for r in self.results)

    @property
    def exit_code(self) -> int:
        return 1 if self.has_fail else 0


CORE_PACKAGES = (
    "numpy",
    "scipy",
    "pandas",
    "matplotlib",
    "PIL",
    "skimage",
    "tqdm",
    "torch",
    "torchvision",
    "monai",
    "torchmetrics",
    "jupyterlab",
    "ipywidgets",
)

JUPYTER_PACKAGES = (
    "jupyterlab",
    "notebook",
    "ipywidgets",
)


def _count_files(directory: Path, extensions: tuple[str, ...]) -> int:
    if not directory.is_dir():
        return 0
    return sum(1 for p in directory.rglob("*") if p.is_file() and p.suffix.lower() in extensions)


def check_directory_structure(cfg: ProjectConfig, report: CheckReport) -> None:
    """Valida existência da estrutura mínima do repositório."""
    markers = [
        ("00-common", cfg.common_dir),
        ("10-docker", cfg.root / "10-docker"),
        ("02-dataset", cfg.data_dir),
    ]
    missing = [name for name, path in markers if not path.exists()]
    if missing:
        report.add(
            Level.FAIL,
            f"Estrutura incompleta — pastas em falta: {', '.join(missing)}",
            "directory_structure",
        )
        return
    report.add(Level.OK, "Estrutura base do repositório validada", "directory_structure")


def create_missing_directories(cfg: ProjectConfig, report: CheckReport) -> None:
    """Cria diretórios obrigatórios em falta."""
    created = []
    for directory in cfg.required_directories:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            created.append(str(directory.relative_to(cfg.root)))
    if created:
        report.add(
            Level.OK,
            f"Diretórios criados ({len(created)}): {', '.join(created[:5])}"
            + (" ..." if len(created) > 5 else ""),
            "create_directories",
        )
    else:
        report.add(Level.OK, "Todos os diretórios obrigatórios já existem", "create_directories")


def check_dataset(cfg: ProjectConfig, report: CheckReport) -> None:
    """Verifica presença de imagens e máscaras no dataset."""
    ext = cfg.dataset_image_extensions
    n_images = _count_files(cfg.images_dir, ext)
    n_masks = _count_files(cfg.masks_dir, ext)

    if n_images == 0 and n_masks == 0:
        report.add(
            Level.WARN,
            "Dataset vazio — coloque ficheiros em 02-dataset/images e 02-dataset/masks",
            "dataset",
        )
        return

    if n_images == 0:
        report.add(Level.WARN, "Nenhuma imagem encontrada em images/", "dataset")
    elif n_masks == 0:
        report.add(Level.WARN, "Nenhuma máscara encontrada em masks/", "dataset")
    else:
        report.add(
            Level.OK,
            f"Dataset encontrado ({n_images} imagens, {n_masks} máscaras)",
            "dataset",
        )

    if n_images > 0 and n_masks > 0 and n_images != n_masks:
        report.add(
            Level.WARN,
            f"Contagem diferente: {n_images} imagens vs {n_masks} máscaras",
            "dataset",
        )


def check_write_permissions(cfg: ProjectConfig, report: CheckReport) -> None:
    """Testa escrita nas pastas de outputs."""
    targets = [
        cfg.preprocessing_output,
        cfg.segmentation_output,
        cfg.evaluation_dir,
        cfg.results_dir,
    ]
    failed = []
    for target in targets:
        target.mkdir(parents=True, exist_ok=True)
        probe = target / ".write_test"
        try:
            probe.write_text("ok", encoding="utf-8")
            probe.unlink(missing_ok=True)
        except OSError:
            failed.append(str(target.relative_to(cfg.root)))

    if failed:
        report.add(
            Level.FAIL,
            f"Sem permissão de escrita em: {', '.join(failed)}",
            "write_permissions",
        )
    else:
        report.add(Level.OK, "Permissões de escrita validadas nos outputs", "write_permissions")


def _import_or_fail(module_name: str) -> tuple[bool, str | None]:
    try:
        importlib.import_module(module_name)
        return True, None
    except ImportError as exc:
        return False, str(exc)


def check_python_dependencies(report: CheckReport) -> None:
    """Verifica imports de pacotes essenciais."""
    missing = []
    for package in CORE_PACKAGES:
        ok, err = _import_or_fail(package)
        if not ok:
            missing.append(f"{package} ({err})")

    if missing:
        report.add(
            Level.FAIL,
            f"Dependências em falta: {', '.join(missing[:4])}"
            + (" ..." if len(missing) > 4 else ""),
            "python_dependencies",
        )
    else:
        report.add(Level.OK, "Dependências Python principais disponíveis", "python_dependencies")


def check_library_versions(report: CheckReport) -> None:
    """Regista versões das bibliotecas principais."""
    versions = []
    for name in ("numpy", "scipy", "pandas", "matplotlib", "skimage", "torch", "monai"):
        try:
            mod = importlib.import_module(name)
            ver = getattr(mod, "__version__", "desconhecida")
            versions.append(f"{name}={ver}")
        except ImportError:
            versions.append(f"{name}=N/A")

    report.add(
        Level.OK,
        "Versões: " + ", ".join(versions[:6]) + (" ..." if len(versions) > 6 else ""),
        "library_versions",
    )


def check_pytorch(report: CheckReport) -> None:
    """Verifica disponibilidade do PyTorch."""
    try:
        import torch
    except ImportError as exc:
        report.add(Level.FAIL, f"PyTorch indisponível: {exc}", "pytorch")
        return

    report.add(
        Level.OK,
        f"PyTorch disponível (v{torch.__version__})",
        "pytorch",
    )


def check_cuda(report: CheckReport, require_gpu: bool = False) -> None:
    """Verifica CUDA e GPU."""
    try:
        import torch
    except ImportError:
        report.add(Level.WARN, "CUDA não verificada — PyTorch em falta", "cuda")
        return

    if torch.cuda.is_available():
        device = torch.cuda.get_device_name(0)
        report.add(Level.OK, f"CUDA disponível ({device})", "cuda")
    elif require_gpu:
        report.add(Level.FAIL, "CUDA indisponível — GPU requerida", "cuda")
    else:
        report.add(
            Level.WARN,
            "CUDA indisponível — execução em CPU (aceitável em desenvolvimento)",
            "cuda",
        )


def check_monai(report: CheckReport) -> None:
    """Verifica MONAI."""
    try:
        import monai
    except ImportError as exc:
        report.add(Level.FAIL, f"MONAI indisponível: {exc}", "monai")
        return

    report.add(Level.OK, f"MONAI disponível (v{monai.__version__})", "monai")


def check_jupyter_stack(report: CheckReport) -> None:
    """Verifica JupyterLab e widgets."""
    missing = []
    for package in JUPYTER_PACKAGES:
        ok, _ = _import_or_fail(package)
        if not ok:
            missing.append(package)

    if missing:
        report.add(
            Level.FAIL,
            f"Stack Jupyter incompleta: {', '.join(missing)}",
            "jupyter_stack",
        )
        return

    report.add(Level.OK, "JupyterLab e ipywidgets configurados", "jupyter_stack")


def check_common_notebooks(cfg: ProjectConfig, report: CheckReport) -> None:
    """Verifica notebooks 00-common."""
    empty = []
    missing = []
    for nb_path in iter_common_notebooks(cfg):
        if not nb_path.exists():
            missing.append(nb_path.name)
        elif nb_path.stat().st_size == 0:
            empty.append(nb_path.name)

    if missing:
        report.add(
            Level.WARN,
            f"Notebooks em falta: {', '.join(missing)}",
            "common_notebooks",
        )
    elif empty:
        report.add(
            Level.WARN,
            f"Notebooks vazios: {', '.join(empty)}",
            "common_notebooks",
        )
    else:
        report.add(Level.OK, "Notebooks 00-common presentes", "common_notebooks")


def print_summary(report: CheckReport, cfg: ProjectConfig) -> None:
    """Resumo final do bootstrap."""
    ok = sum(1 for r in report.results if r.level == Level.OK)
    warn = sum(1 for r in report.results if r.level == Level.WARN)
    fail = sum(1 for r in report.results if r.level == Level.FAIL)

    print()
    print("=" * 60)
    print("Bootstrap — fetal_vein_segmentation")
    print("=" * 60)
    print(f"Raiz do projeto : {cfg.root}")
    print(f"Modo strict     : {cfg.strict_mode}")
    print(f"Resumo          : {ok} OK | {warn} WARN | {fail} FAIL")
    print("=" * 60)

    if report.has_fail and cfg.strict_mode:
        print("Bootstrap terminou com erros (modo strict).")
    elif report.has_fail:
        print("Bootstrap concluído com falhas (modo não strict).")
    else:
        print("Bootstrap concluído com sucesso.")
