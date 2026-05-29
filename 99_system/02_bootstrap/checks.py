"""Verificações de ambiente e estrutura do projeto."""

from __future__ import annotations

import importlib
import os
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Iterable

from config import ProjectConfig, iter_common_notebooks, normalize_profile


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


CPU_PACKAGES = (
    "numpy",
    "scipy",
    "pandas",
    "matplotlib",
    "PIL",
    "skimage",
    "tqdm",
    "jupyterlab",
    "ipywidgets",
)

GPU_PACKAGES = (
    "torch",
    "torchvision",
    "monai",
    "torchmetrics",
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
        ("00_common", cfg.common_dir),
        ("99_system/01_runtime", cfg.runtime_dir),
        ("04_segmentation", cfg.root / "04_segmentation"),
        ("02_dataset", cfg.data_dir),
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
            "Dataset vazio — coloque ficheiros em 02_dataset/images e 02_dataset/labels",
            "dataset",
        )
        return

    if n_images == 0:
        report.add(Level.WARN, "Nenhuma imagem encontrada em images/", "dataset")
    elif n_masks == 0:
        report.add(Level.WARN, "Nenhuma máscara encontrada em labels/ (ou masks/)", "dataset")
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


def check_python_dependencies(cfg: ProjectConfig, report: CheckReport) -> None:
    """Verifica imports de pacotes essenciais.

    - Perfil CPU: falha apenas se faltar o stack CPU/Jupyter.
    - Perfil GPU: falha também se faltar PyTorch/MONAI/TorchMetrics.
    """
    missing_cpu = []
    for package in CPU_PACKAGES:
        ok, err = _import_or_fail(package)
        if not ok:
            missing_cpu.append(f"{package} ({err})")

    missing_gpu = []
    for package in GPU_PACKAGES:
        ok, err = _import_or_fail(package)
        if not ok:
            missing_gpu.append(f"{package} ({err})")

    if missing_cpu:
        report.add(
            Level.FAIL,
            f"Dependências CPU/Jupyter em falta: {', '.join(missing_cpu[:4])}"
            + (" ..." if len(missing_cpu) > 4 else ""),
            "python_dependencies",
        )
        return

    if missing_gpu and cfg.requires_gpu_stack:
        report.add(
            Level.FAIL,
            f"Dependências GPU em falta: {', '.join(missing_gpu[:4])}"
            + (" ..." if len(missing_gpu) > 4 else ""),
            "python_dependencies",
        )
        return

    if missing_gpu and not cfg.requires_gpu_stack:
        report.add(
            Level.WARN,
            "Dependências GPU ausentes (esperado no perfil CPU): "
            + ", ".join(m.split(" (")[0] for m in missing_gpu),
            "python_dependencies",
        )
        return

    report.add(Level.OK, "Dependências Python validadas para o perfil ativo", "python_dependencies")


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


def check_pytorch_profile(cfg: ProjectConfig, report: CheckReport) -> None:
    """PyTorch como WARN no CPU e FAIL no GPU."""
    try:
        import torch  # noqa: F401
    except ImportError as exc:
        level = Level.FAIL if cfg.requires_gpu_stack else Level.WARN
        report.add(level, f"PyTorch indisponível: {exc}", "pytorch")
        return
    report.add(Level.OK, "PyTorch disponível", "pytorch")


def check_monai_profile(cfg: ProjectConfig, report: CheckReport) -> None:
    """MONAI como WARN no CPU e FAIL no GPU."""
    try:
        import monai  # noqa: F401
    except ImportError as exc:
        level = Level.FAIL if cfg.requires_gpu_stack else Level.WARN
        report.add(level, f"MONAI indisponível: {exc}", "monai")
        return
    report.add(Level.OK, "MONAI disponível", "monai")


def check_cuda_profile(cfg: ProjectConfig, report: CheckReport) -> None:
    """CUDA como WARN no local-cpu e FAIL nos perfis GPU."""
    check_cuda(report, require_gpu=cfg.requires_gpu_stack)


def check_runtime_adapters(cfg: ProjectConfig, report: CheckReport) -> None:
    """Valida adapters e configs dos runtimes."""
    runtime_files = [
        "local_cpu/adapter.py",
        "local_cpu/config.yaml",
        "local_gpu/adapter.py",
        "local_gpu/config.yaml",
        "kaggle/adapter.py",
        "kaggle/config.yaml",
        "entrypoint.sh",
    ]
    missing = [
        rel for rel in runtime_files if not (cfg.runtime_dir / rel).exists()
    ]
    if missing:
        report.add(
            Level.FAIL,
            f"Runtime incompleto — ficheiros em falta: {', '.join(missing)}",
            "runtime_adapters",
        )
        return
    report.add(
        Level.OK,
        "Runtimes local_cpu, local_gpu e kaggle presentes",
        "runtime_adapters",
    )


def check_segmentation_pipeline(cfg: ProjectConfig, report: CheckReport) -> None:
    """Garante que a pipeline única de treino existe."""
    pipeline_files = ("train.py", "dataset.py", "model.py", "config.yaml")
    seg_dir = cfg.root / "04_segmentation"
    missing = [name for name in pipeline_files if not (seg_dir / name).exists()]
    if missing:
        report.add(
            Level.FAIL,
            f"Pipeline 04_segmentation incompleta: {', '.join(missing)}",
            "segmentation_pipeline",
        )
        return
    report.add(Level.OK, "Pipeline única 04_segmentation validada", "segmentation_pipeline")


def check_kaggle_environment(cfg: ProjectConfig, report: CheckReport) -> None:
    """Validações específicas do perfil Kaggle."""
    if cfg.normalized_profile != "kaggle":
        return

    if not Path("/kaggle").exists():
        report.add(
            Level.WARN,
            "Perfil kaggle ativo mas /kaggle não existe (execução local de teste)",
            "kaggle_environment",
        )
        return

    input_dir = Path("/kaggle/input")
    if input_dir.is_dir():
        datasets = [p.name for p in input_dir.iterdir() if p.is_dir()]
        if datasets:
            report.add(
                Level.OK,
                f"Datasets Kaggle montados: {', '.join(datasets[:5])}",
                "kaggle_environment",
            )
        else:
            report.add(Level.WARN, "Nenhum dataset em /kaggle/input", "kaggle_environment")
    else:
        report.add(Level.WARN, "/kaggle/input indisponível", "kaggle_environment")

    if Path("/kaggle/working").is_dir():
        report.add(Level.OK, "/kaggle/working disponível para outputs", "kaggle_environment")


def run_runtime_adapter_validation(cfg: ProjectConfig, report: CheckReport) -> None:
    """Executa validate_runtime() do adapter ativo."""
    adapter_py = cfg.runtime_adapter_dir / "adapter.py"
    if not adapter_py.exists():
        report.add(Level.WARN, f"Adapter em falta: {adapter_py}", "runtime_validation")
        return

    import importlib.util

    spec = importlib.util.spec_from_file_location("runtime_adapter", adapter_py)
    if spec is None or spec.loader is None:
        report.add(Level.WARN, "Não foi possível carregar adapter", "runtime_validation")
        return

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "prepare_environment"):
        try:
            module.prepare_environment(cfg.root)
        except Exception as exc:
            report.add(Level.WARN, f"prepare_environment falhou: {exc}", "runtime_validation")

    if not hasattr(module, "validate_runtime"):
        report.add(Level.WARN, "Adapter sem validate_runtime()", "runtime_validation")
        return

    issues = module.validate_runtime(cfg.root)
    if issues:
        level = Level.FAIL if cfg.strict_mode else Level.WARN
        for issue in issues:
            report.add(level, issue, "runtime_validation")
    else:
        profile = normalize_profile(cfg.profile)
        report.add(Level.OK, f"Adapter {profile} validado", "runtime_validation")


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
    """Verifica notebooks 00_common."""
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
        report.add(Level.OK, "Notebooks 00_common presentes", "common_notebooks")


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
    print(f"Perfil runtime  : {cfg.normalized_profile}")
    print(f"Modo strict     : {cfg.strict_mode}")
    print(f"Resumo          : {ok} OK | {warn} WARN | {fail} FAIL")
    print("=" * 60)

    if report.has_fail and cfg.strict_mode:
        print("Bootstrap terminou com erros (modo strict).")
    elif report.has_fail:
        print("Bootstrap concluído com falhas (modo não strict).")
    else:
        print("Bootstrap concluído com sucesso.")
